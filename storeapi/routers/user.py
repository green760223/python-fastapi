import logging

from fastapi import APIRouter, HTTPException, status

from storeapi.database import database, user_table
from storeapi.models.user import UserIn
from storeapi.security import get_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )

    query = user_table.insert().values(email=user.email, password=user.password)

    logger.debug(query)

    await database.execute(query)

    return {"detail": "User created successfully"}
