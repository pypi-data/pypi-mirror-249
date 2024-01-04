import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from loguru import logger

from optrabot import config
from .optrabot import OptraBot
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
	await app.optraBot.startup()
	yield
	await app.optraBot.shutdown()

"""fix yelling at me error"""
from functools import wraps
 
from asyncio.proactor_events import _ProactorBasePipeTransport
 
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
 
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

app = FastAPI(lifespan=lifespan)
app.optraBot = OptraBot(app)

@app.get("/")
async def root():
	return "Welcome to OptraBot"

if __name__ == '__main__':
	if config.ensureInitialConfig()	== True:
		# Get web port from config
		configuration = config.Config("config.yaml")
		webPort: int
		try:
			webPort = configuration.get('general.port')
		except KeyError as keyErr:
			webPort = 8080
		uvicorn.run("optrabot.main:app", port=int(webPort), log_level="info")
	else:
		print("Configuration error. Unable to run OptraBot!")