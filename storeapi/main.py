from contextlib import asynccontextmanager

from fastapi import FastAPI

from storeapi.database import database
from storeapi.routers.post import router as post_router


# The lifespan context manager is used to connect and disconnect from the database.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


#
app = FastAPI(lifespan=lifespan)

# Include the post router in the app
app.include_router(post_router)
