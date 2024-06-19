import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

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
app.add_middleware(CorrelationIdMiddleware)

# Include the post router in the app
app.include_router(post_router)


# The exception handler logs the exception and then calls the default exception handler.
@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
