import asyncio
from optrabot import config
from optrabot.config import Config
from contextlib import suppress
import datetime as dt
from datetime import datetime, timezone
from ib_insync import *
import json
from loguru import logger
import httpx

from optrabot.marketdatatype import MarketDataType
from optrabot.optionhelper import OptionHelper

class TradinghubClient():
	def __init__(self, optraBot):
		logger.debug("TradinghubClient Init")
		self._lastAnswerReceivedAt = None
		self.optraBot = optraBot
		if self.optraBot:
			self._config : Config = self.optraBot['config']
		else:
			self._config = Config()
		self._agentId = ''
		self.hub_host = ''
		self._contracts: int = 0
		try:
			self._contracts = int(self._config.get('tws.contracts'))
		except KeyError as keyErr:
			self._contracts = 1
		self._accountNo = None
		self._entryTrade = None
		self._entryTradeContract = None
		self._slShortTrade = None
		self._tpTrade = None
		self._ironFlyAskPrice = 0.0
		self._ironFlyComboContract = None
		self._ironFlyLongLegContracts = None
		self._ironFlyShortComboContract = None
		self._longLegFillsPrice = 0.0
		self._longLegFillsReceived = 0
		self._shuttingdown = False
		self._minimumPremium = None
		self._positionMonitorTask = None
		self._position = False
		
	async def shutdown(self):
		logger.info('Shutting down Trading Hub Client.')
		self._shuttingdown = True
		self._stopPositionMonitoring()

	async def _poll(self):
		try:
			fetch_url = self.hub_host + '/fetch_signal'
			url_params = {'agentid': self._agentId}
			headers = {'X-API-Key': self._apiKey, 'X-Version': self.optraBot.Version}
			#if self.client_session.closed == True:
			#	logger.debug("Client Session closed. Stop polling.")
			#	return
			if self._shuttingdown:
				logger.debug("Client Session closed. Stop polling.")
				return
			
			logger.debug('Checking for Signal from Hub.')
			response = httpx.get(fetch_url, params=url_params, follow_redirects=True, headers=headers)
			#self._client_session = ClientSession()	
			#async with self._client_session.get(fetch_url, params=url_params) as resp:
			#	await asyncio.sleep(0.001)
			#	response = await resp.text()
			logger.debug('Answer received ({}).', response.status_code)
			if response.status_code != 200:
				logger.error("Error on HTTP request: {}", response.reason_phrase)
				await self._scheduleNextPoll()
				return

			self._lastAnswerReceivedAt = datetime.now()
			if response.text != '\"\"' and response.text != '':
				logger.debug("Response {}", response.content )

				try:
					response_data = json.loads(response.content)
				except json.JSONDecodeError as jsonExcp:
					logger.error("Didn't receive JSON data!")
					await self._scheduleNextPoll()
					return

				# Check for the Signal 0DTEIronFly	
				if response_data['strategy'] != '0DTEIronFly':
					logger.error('Strategy: {} is not supported!', response_data['strategy'])
					await self._scheduleNextPoll()
					return

				signalTime = self._parseTimestamp(response_data['time'])
				if signalTime == None or self._signalIsOutdated(signalTime):
					logger.warning('Signal is outdated already or Signal timestamp is invalid!')
					await self._scheduleNextPoll()
					return

				logger.info('Received Signal: {}', response_data['strategy'])
				try:
					ib: IB = self.optraBot['ib']
					if not ib.isConnected():
						logger.error("Interactive Brokers is not connected. Unable to process received signal!")
						await self._scheduleNextPoll()
						return
					
					if not self.optraBot.isTradingEnabled():
						logger.error("Trading is not enabled. Looks like your Market Data Subscription is wrong. Skippimg this Trade!")
						await self._scheduleNextPoll()
						return

					spx = Index('SPX', 'CBOE')
					qualifiedContracts = await ib.qualifyContractsAsync(spx) 
					[ticker] = await ib.reqTickersAsync(spx)
					spxValue = ticker.marketPrice()
					#self.app['SPXPrice'] = spxValue
					logger.debug("SPX Market Price {}", spxValue)

					chains = await ib.reqSecDefOptParamsAsync(spx.symbol, '', spx.secType, spx.conId)
					chain = next(c for c in chains if c.tradingClass == 'SPXW' and c.exchange == 'SMART')
					if chain == None:
						logger.error("No Option Chain for SPXW and CBOE found! Doing no trade!")
						await self._scheduleNextPoll()
						return
					
					# Options Kontrakte ermitteln
					nan = float('nan')
					wingSize = 70.0
					amount = self._contracts
					accountNo = self._accountNo
					current_date = dt.date.today()
					expiration = current_date.strftime('%Y%m%d')
					shortLegStrike = float(response_data['vwaptarget'])
					longPutStrike = shortLegStrike - wingSize
					longCallStrike = shortLegStrike + wingSize
					logger.info("Building Iron Fly combo with Short strike {}, Long Put strike {} and Long Call strike {}", shortLegStrike, longPutStrike, longCallStrike)
					
					shortPutContract = Option(spx.symbol, expiration, shortLegStrike, 'P', 'SMART', tradingClass = 'SPXW')
					await ib.qualifyContractsAsync(shortPutContract)
					if not OptionHelper.checkContractIsQualified(shortPutContract):
						return

					shortCallContract = Option(spx.symbol, expiration, shortLegStrike, 'C', 'SMART', tradingClass = 'SPXW')				
					await ib.qualifyContractsAsync(shortCallContract)
					if not OptionHelper.checkContractIsQualified(shortCallContract):
						return
						
					longPutContract = Option(spx.symbol, expiration, longPutStrike, 'P', 'SMART', tradingClass = 'SPXW')
					await ib.qualifyContractsAsync(longPutContract)
					if not OptionHelper.checkContractIsQualified(longPutContract):
						return

					longCallContract = Option(spx.symbol, expiration, longCallStrike, 'C', 'SMART', tradingClass = 'SPXW')
					await ib.qualifyContractsAsync(longCallContract)
					if not OptionHelper.checkContractIsQualified(longCallContract):
						return

					self._ironFlyLongLegContracts = [longCallContract, longPutContract]
					ironFlyContracts = [shortPutContract, shortCallContract, longPutContract, longCallContract]
					ironFlyComboContract = Contract(symbol=spx.symbol, secType='BAG', exchange='SMART', currency='USD',
						comboLegs=[
							#ComboLeg(conId=shortPutContract.conId, ratio=1, action='SELL', exchange='SMART'),
							#ComboLeg(conId=shortCallContract.conId, ratio=1, action='SELL' , exchange='SMART'),
							#ComboLeg(conId=longPutContract.conId, ratio=1, action='BUY', exchange='SMART'),
							#ComboLeg(conId=longCallContract.conId, ratio=1, action='BUY', exchange='SMART')
						]
					)

					self._ironFlyShortComboContract = Contract(symbol=spx.symbol, secType='BAG', exchange='SMART', currency='USD', comboLegs=[])

					ironFlyMidPrice = 0.0
					tickers = await ib.reqTickersAsync(*ironFlyContracts)
					for ticker in tickers:
						tickerContract = ticker.contract
						if tickerContract.conId == shortPutContract.conId:
							midPrice = (ticker.ask + ticker.bid) / 2
							if util.isNan(midPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
								midPrice = 100
							ironFlyMidPrice -= midPrice
							if not util.isNan(ticker.bid):
								self._ironFlyAskPrice -= ticker.bid
							ironFlyComboContract.comboLegs.append(ComboLeg(conId=shortPutContract.conId, ratio=1, action='SELL', exchange='SMART'))
							self._ironFlyShortComboContract.comboLegs.append(ComboLeg(conId=shortPutContract.conId, ratio=1, action='BUY', exchange='SMART'))
						if tickerContract.conId == shortCallContract.conId:
							midPrice = (ticker.ask + ticker.bid) / 2
							if util.isNan(midPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
								midPrice = 100
							ironFlyMidPrice -= midPrice
							if not util.isNan(ticker.bid):
								self._ironFlyAskPrice -= ticker.bid
							ironFlyComboContract.comboLegs.append(ComboLeg(conId=shortCallContract.conId, ratio=1, action='SELL', exchange='SMART'))
							self._ironFlyShortComboContract.comboLegs.append(ComboLeg(conId=shortCallContract.conId, ratio=1, action='BUY', exchange='SMART'))
						if tickerContract.conId == longPutContract.conId:
							midPrice = (ticker.ask + ticker.bid) / 2
							if util.isNan(midPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
								midPrice = 0.05
							ironFlyMidPrice += midPrice
							if not util.isNan(ticker.ask):
								self._ironFlyAskPrice += ticker.ask
							ironFlyComboContract.comboLegs.append(ComboLeg(conId=longPutContract.conId, ratio=1, action='BUY', exchange='SMART'))
						if tickerContract.conId == longCallContract.conId:
							midPrice = (ticker.ask + ticker.bid) / 2
							if util.isNan(midPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
								midPrice = 0.05
							ironFlyMidPrice += midPrice
							if not util.isNan(ticker.ask):
								self._ironFlyAskPrice += ticker.ask
							ironFlyComboContract.comboLegs.append(ComboLeg(conId=longCallContract.conId, ratio=1, action='BUY', exchange='SMART'))

					logger.debug("Tickers {}", tickers)
					ticker = tickers[0]
					if util.isNan(ironFlyMidPrice):
						logger.error("No Mid Price for combo could be calculated!")
						await self._scheduleNextPoll()
						return

					limitPrice = OptionHelper.roundToTickSize(ironFlyMidPrice)

					logger.info("IronFly Combo Mid Price: {} Ask Price: {}", ironFlyMidPrice, self._ironFlyAskPrice)

					if not self._meetsMinimumPremium(limitPrice):
						logger.info('Premium below configured minimum premium of ${}. Trade is not executed!', self._minimumPremium)
					else:
						order = LimitOrder('BUY', amount, limitPrice)
						order.account = accountNo
						order.orderRef = 'OTB: IF - Open'
						order.outsideRth = True
						self._entryTrade = ib.placeOrder(ironFlyComboContract, order)
						self._entryTrade.statusEvent += self.onOrderStatusEvent
						self._entryTradeContract = ironFlyComboContract
						self._ironFlyComboContract = ironFlyComboContract
						self._ironFlyAskPrice = 0.0
						self._longLegFillsPrice = 0.0
						self._longLegFillsReceived = 0
						self._slShortTrade = None
						self._tpTrade = None
						logger.debug("Account: {} Trade placed: {} Number of contracts: {}", order.account, self._entryTrade, amount)
						asyncio.create_task(self._trackEntryOrder())

				except Exception as excp:
						logger.error("Exception: {}", excp)

		except Exception as anyEcxp:
			logger.error("Exception occured during poll: {}", anyEcxp)

		await self._scheduleNextPoll()

	async def _trackEntryOrder(self):
		await asyncio.sleep(5) # Wait 5 seconds for order Execution
		ib: IB = self.optraBot['ib']
		if self._entryTrade == None:
			return
		
		if self._entryTrade.orderStatus.status == OrderStatus.Cancelled or self._entryTrade.orderStatus.status == OrderStatus.Inactive:
			logger.info("Entry Order was cancelled by someone else!")
			self._entryTrade = None
		elif self._entryTrade.orderStatus.status == OrderStatus.Filled:
			logger.info("Entry Order has been filled already. No adjustment required")
		else:
			currentLimitPrice = self._entryTrade.order.lmtPrice
			adjustedLimitPrice = currentLimitPrice + self._priceAdjustmentStep
			logger.info("Entry Order status ({}). Entry price will be adjusted. Current Limit Price: ${}", self._entryTrade.orderStatus.status, currentLimitPrice)
			if self._meetsMinimumPremium(adjustedLimitPrice) and adjustedLimitPrice <= self._ironFlyAskPrice:
				#self.entryOrderAdjustments += 1	
				self._entryTrade.order.lmtPrice = adjustedLimitPrice
				try:
					ib.placeOrder(self._entryTradeContract, self._entryTrade.order)
					asyncio.create_task(self._trackEntryOrder())
				except Exception as excp:
					logger('Exception beim Anpassen der Order')
			else:
				if adjustedLimitPrice > -15:
					logger.info("Entry order limit price reached minimum premium. No entry.")
				if adjustedLimitPrice > self._ironFlyAskPrice:
					logger.info("Entry order limit price exceeded initial ask price. No entry.")
				ib.cancelOrder(self._entryTrade.order)

	async def onOrderStatusEvent(self, trade: Trade):
		if trade == self._entryTrade:
			logger.debug('Order Status Event has been raised. Status: {}', trade.orderStatus.status)
			if trade.orderStatus.status == OrderStatus.Cancelled:
				logger.info('Entry Order has been cancelled!')
				self._entryTrade = None
			elif trade.orderStatus.status == OrderStatus.Filled and self._position == False:
				logger.info('Entry Order has been filled at ${} (Qty: {}) and trade is running now.', trade.orderStatus.avgFillPrice, trade.orderStatus.filled)
				self._position = True
				task = asyncio.create_task(self._placeTakeProfitAndStop(trade))
				#Run 1. Position Monitoring with delay
				self._positionMonitorTask = asyncio.create_task(self._monitorPositionDelayed())
			elif trade.orderStatus.status == OrderStatus.Filled and self._position == True:
				logger.debug('Additionally fill quantity (Qty: {}) for the entry order...depending orders need to be adjusted.', trade.orderStatus.filled)
				if trade.orderStatus.remaining > 0:
					logger.warning('Entry Order was filled partially only!')
				asyncio.create_task(self._adjustTakeProfitAndStop(trade))

		elif trade == self._tpTrade:
			logger.debug('TP Order Status has been raised. Status: {}', trade.orderStatus.status)
			if trade.orderStatus.status == OrderStatus.Cancelled:
				logger.info('TP Order has been cancelled!')
				self._tpTrade = None
			elif trade.orderStatus.status == OrderStatus.Filled:
				logger.info('TP Order has been filled. Trade finished')
				self._tpTrade = None
				self._slShortTrade = None
				self._onPositionClose()
		elif trade == self._slShortTrade:
			logger.debug('SL order for Short Legs status has been changed. Status: {}', trade.orderStatus.status)
			if trade.orderStatus.status == OrderStatus.Cancelled:
				logger.info('SL order for Short Legs has been cancelled!')
				self._slShortTrade = None
			elif trade.orderStatus.status == OrderStatus.Filled:
				logger.info('SL order for Short Legs has been filled. Trade finished')
				logger.info('Now....Long Legs need to be closed if possible')
				await self._close_long_legs()
				self._onPositionClose()

	async def onExecDetailsEvent(self, trade: Trade, fill: Fill):
		if trade == self._entryTrade:
			#TODO: Remove code below, because not needed anymore
			return
			logger.debug('Received ExecDetails for Entry Order: {}', fill)
			for comboLeg in self._entryTradeContract.comboLegs:
				if comboLeg.action == 'BUY' and fill.contract.conId == comboLeg.conId:
					logger.debug('Long Leg fill at {}', fill.execution.price)
					self._longLegFillsPrice += fill.execution.price
					self._longLegFillsReceived += 1
			
			if self._longLegFillsReceived == 2 and self._slShortTrade == None:
				logger.debug('Received both long leg execution details. Long Legs filled at ${}', self._longLegFillsPrice)

				#if self._slShortTrade != None:
				ib: IB = self.app['ib']
				shortsStopPrice = (self._entryTrade.orderStatus.avgFillPrice * -1.16) + (self._longLegFillsPrice/2)
				roundBase = 5
				shortsStopPrice = (roundBase * round(shortsStopPrice*100/roundBase)) / 100
				logger.debug('Stop price for short legs: ${}', shortsStopPrice) 
				#stopShortsOrder = StopOrder('BUY', self._entryTrade.orderStatus.filled, shortsStopPrice)
				#REMOVE BEFORE FLIGHT
				stopShortsOrder = LimitOrder('BUY', self._entryTrade.orderStatus.filled, 10)
				stopShortsOrder.account = self._accountNo
				stopShortsOrder.orderRef = 'IF: SL Short Legs'
				stopShortsOrder.ocaGroup = self._ocaGroup
				try:
					self._slShortTrade = ib.placeOrder(self._ironFlyShortComboContract, stopShortsOrder)
					self._slShortTrade.statusEvent += self.onOrderStatusEvent
				except Exception as excp:
						logger('Exception beim Erstellen der Short Leg Stoploss order')
				#	self._slShortTrade.order.auxPrice += fill.execution.price
				#	try:
				#		ib.placeOrder(self._ironFlyShortComboContract, self._slShortTrade.order)
				#	except Exception as excp:
				#		logger('Exception beim Anpassen der Order')

	async def _placeTakeProfitAndStop(self, entryTrade: Trade):
		fillPrice = entryTrade.orderStatus.avgFillPrice
		fillAmount = entryTrade.orderStatus.filled
		logger.debug('Entry Order was filled at ${}', fillPrice)
		if entryTrade.orderStatus.remaining > 0:
			logger.warning('Entry Order was filled partially only.')
		ib: IB = self.optraBot['ib']

		# Calculate Take Profit price
		try:
			profitLevel = int(self._config.get('tws.takeprofit'))
		except KeyError as keyErr:
			profitLevel = 8
		try:
			stopLevel = int(self._config.get('tws.stoploss'))
		except KeyError as keyErr:
			stopLevel = 16
		logger.debug('Using Profit Level {} and Stop Level {}', profitLevel, stopLevel)
		profit = fillPrice * (profitLevel / 100)

		limitPrice = OptionHelper.roundToTickSize(fillPrice - profit)
		now = datetime.now()
		self._ocaGroup = self._accountNo + '_' + now.strftime('%H%M%S')
		logger.info('Take Profit Limit Price ({}%) : {}', profitLevel, limitPrice)
		order = LimitOrder('SELL', fillAmount, limitPrice)
		order.account = self._accountNo
		order.orderRef = 'OTB: IF - Take Profit'
		order.ocaGroup = self._ocaGroup
		order.outsideRth = True
		self._tpTrade = ib.placeOrder(self._ironFlyComboContract, order)
		self._tpTrade.statusEvent += self.onOrderStatusEvent

		# Calculation of Stop Price
		stopFactor = ((stopLevel / 100) + 1) * -1
		self._ironFlyStopPrice = OptionHelper.roundToTickSize(fillPrice * stopFactor)
		logger.info('Stop LossPrice ({}%): {}', stopLevel, self._ironFlyStopPrice)

		stopShortsOrder = StopOrder('BUY', self._entryTrade.orderStatus.filled, self._ironFlyStopPrice)
		stopShortsOrder.account = self._accountNo
		stopShortsOrder.orderRef = 'OTB IF - SL Short Legs'
		stopShortsOrder.ocaGroup = self._ocaGroup
		try:
			self._slShortTrade = ib.placeOrder(self._ironFlyShortComboContract, stopShortsOrder)
			self._slShortTrade.statusEvent += self.onOrderStatusEvent
		except Exception as excp:
			logger('Exception beim Erstellen der Short Leg Stoploss order')

	async def _adjustTakeProfitAndStop(self, trade: Trade):
		""" Adjust Take Profit and Stop Order after another partial fill of the entry Order.
		"""
		ib: IB = self.optraBot['ib']
		newQuantity = trade.orderStatus.filled
		logger.info('Adjusting quantity of TP and Stop Order to {}', newQuantity)
		self._tpTrade.order.totalQuantity = trade.orderStatus.filled
		ib.placeOrder(self._tpTrade.contract, self._tpTrade.order)
		self._slShortTrade.order.totalQuantity = trade.orderStatus.filled
		ib.placeOrder(self._slShortTrade.contract, self._slShortTrade.order)

	async def _close_long_legs(self):
		logger.debug("Closing long legs of trade")
		ib: IB = self.optraBot['ib']
		tickers = await ib.reqTickersAsync(*self._ironFlyLongLegContracts)
		for ticker in tickers:
			logger.debug("Long Leg {} {} Bid Price: {}", ticker.contract.right, ticker.contract.strike, ticker.bid)
			if ticker.bid >= 0.05:
				logger.debug('Creating limit sell order on bid Price')
				order = LimitOrder('SELL', self._entryTrade.orderStatus.filled, ticker.bid)
				order.orderRef = 'OTB: IF - Close Long Leg'
				ib.placeOrder(ticker.contract, order)

	def _onPositionClose(self):
		logger.debug('_onPositionClose()')
		self._tpTrade = None
		self._slShortTrade = None
		self._entryTrade = None
		self._ironFlyComboContract = None
		self._position = False
		self._stopPositionMonitoring()

	async def _monitorPosition(self):
		logger.debug('Monitor position()')
		if self._position == False:
			logger.debug('Position has been closed. Stopping Position-Monitoring now.')
			self._positionMonitorTask = None
			return

		asyncio.create_task(self._monitorPositionDelayed())

		ib: IB = self.optraBot['ib']
		tickers = await ib.reqTickersAsync(*self._ironFlyLongLegContracts)
		longLegsValue = 0
		for ticker in tickers:
			if ticker.bid >= 0:
				longLegsValue += ticker.bid
		desiredStopPrice = OptionHelper.roundToTickSize(self._ironFlyStopPrice - longLegsValue)
		currentStopPrice = OptionHelper.roundToTickSize(self._slShortTrade.order.auxPrice)
		logger.debug('Long Legs value {} Current Short SL Price: {} Desired Short SL Pice: {}', round(longLegsValue,2), currentStopPrice, desiredStopPrice)
		if currentStopPrice != desiredStopPrice:
			self._slShortTrade.order.auxPrice = desiredStopPrice
			logger.info('Adjusting Stop Loss price to ${}', desiredStopPrice)
			ib.placeOrder(self._slShortTrade.contract, self._slShortTrade.order)
		else:
			logger.debug('No adjustment of Stop Loss price required.')

	async def _monitorPositionDelayed(self):
		logger.debug('Waiting 10 seconds for next position monitoring.')
		await asyncio.sleep(10)
		self._positionMonitorTask = asyncio.create_task(self._monitorPosition())

	def _meetsMinimumPremium(self, premium: float) -> bool:
		""" Checks if given premium meets minimum premium

		Parameters
		----------
		premium : float
			As premium is a typically a credit, a negative number is expected.
		
		Returns
		-------
		bool
			Returns True, if the received premium is more than the configured minimum premium
		"""
		if self._minimumPremium == None:
			try:
				self._minimumPremium = self._config.get('tws.minimumPremium')
			except KeyError as keyError:
				self._minimumPremium = 0.0
		if premium > (self._minimumPremium * -1):
			return False
		return True

	def _parseTimestamp(self, timestamp: str) -> datetime:
		""" Parses the given timestamp into a `datetime`object

		Parameters
		----------
		timestamp : str
    		Timestamp as string with timezone info e.g. 2023-11-07T14:10:00Z.
		"""
		try:
			parsedTime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
		except Exception as excpt:
			logger.error("Timestamp {} got unexpected format.", timestamp)
			return None
		return parsedTime


	def _signalIsOutdated(self, signalTimeStamp: datetime):
		""" Checks if the time stamp of the signal is older than 10 minutes which means it's outdated.
		
		Parameters
		----------
		signalTimeStamp : datetime
    		Timestamp of the signal.

		Returns
		-------
		bool
			Returns True, if the signal is outdated
		"""
		if datetime == None:
			return True
		currentTime = datetime.now().astimezone()
		timediff = currentTime - signalTimeStamp
		if (timediff.seconds / 60) > 10:
			return True
		return False

	async def _scheduleNextPoll(self):
		await asyncio.sleep(5)
		task = asyncio.create_task(self._poll())

	async def start_polling(self):
		"""
		Tradinghub Polling runner
		"""
		logger.debug("start_polling")

		try:
			self.hub_host = self._config.get('general.hub')
		except KeyError as keyError:
			self.hub_host = config.defaultHubHost
			logger.warning("No Hub URL is configured in config.yaml. Using the default.")

		try:
			self._apiKey = self._config.get('general.apikey')
		except KeyError as keyError:
			logger.error("No API Key is configured in config.yaml. Stopping here!")
			return

		try:
			self._agentId = self._config.get('general.agentid')
			logger.info("Running with Agent ID '{}'.", self._agentId)
		except KeyError as keyError:
			self._agentId = None
		if self._agentId == None:
			logger.error("No Agent ID configured in config.yaml. Stop polling!")
			return
		
		try:
			self._accountNo = self._config.get('tws.account')
			logger.info('Configured TWS account: {}', self._accountNo)
		except KeyError as keyError:
			self._accountNo = None
		if self._accountNo == None:
			logger.error('Missing TWS account number in config.yaml')
			return
		
		try:
			self._priceAdjustmentStep = self._config.get('tws.adjustmentstep')
		except KeyError as keyError:
			self._priceAdjustmentStep = 0.05

		# Register for Execution Details Event
		#ib: IB = self.optraBot['ib']
		#if not ib.isConnected():
		#	logger.error("Interactive Brokers is not connected. Unable to process received signal!")
		#	return
		#TODO: Einkommentieren
		#ib.execDetailsEvent+= self.onExecDetailsEvent
		#ib.pendingTickersEvent += self.onPendingTickersEvent

		try:
			tasks: List[asyncio.Task[Any]] = [
				asyncio.create_task(self._poll())
			]
			#tasks.append(asyncio.create_task(self._stop_signal.wait()))
			done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

			for task in pending:
				# (mostly) Graceful shutdown unfinished tasks
				task.cancel()
				with suppress(asyncio.CancelledError):
					await task
				# Wait finished tasks to propagate unhandled exceptions
				await asyncio.gather(*done)
		except Exception as excp:
			logger.error("Exception {}", excp)

	def _stopPositionMonitoring(self):
		if self._positionMonitorTask:
			self._positionMonitorTask.cancel()
			self._positionMonitorTask = None

	def isHubConnectionOK(self) -> bool:
		""" Returns True if the last request to the OptraBot Hub was responed 
		30 seconds ago or less.
		"""
		if self._lastAnswerReceivedAt == None:
			return False
		timeDelta = datetime.now() - self._lastAnswerReceivedAt
		if timeDelta.total_seconds() > 30:
			return False
		else:
			return True