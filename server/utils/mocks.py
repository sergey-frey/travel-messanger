def get_session():
    raise NotImplementedError

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

# from db.models import User


# async def get_user_db(session: AsyncSession = Depends(get_session)):
#     yield SQLAlchemyUserDatabase(session, User)