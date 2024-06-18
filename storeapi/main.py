import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


# The lifespan context manager is used to connect and disconnect from the database.
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Hello world")
    await database.connect()
    yield
    await database.disconnect()


#
app = FastAPI(lifespan=lifespan)

# Include the post router in the app
app.include_router(post_router)
