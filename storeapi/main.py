import logging
from contextlib import asynccontextmanager

import sentry_sdk
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from storeapi.config import config
from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router
from storeapi.routers.upload import router as upload_router
from storeapi.routers.user import router as user_router

# Sentry SDK is used to capture errors and performance data.
sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

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
app.include_router(user_router)
app.include_router(upload_router)


# This route triggers a division by zero error to test Sentry.
# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0
#     return division_by_zero


# The exception handler logs the exception and then calls the default exception handler.
@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
