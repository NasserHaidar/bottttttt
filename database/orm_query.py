from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from database.models.user import User


async def orm_add_user(session: AsyncSession , data: dict):
    obj = User(
        id=data["id"],
        name=data["name"],
        status_subscription=data["status_sub"],
        balance=data["balance"],
        image=data["image"],
        date=data["date"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalar().all()

async def orm_get_user(session:AsyncSession , user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user(session:AsyncSession, user_id: int, data):
    query = update(User).where(User.id == user_id).values(
        id=data["id"],
        name=data["name"],
        status_subscription=data["status_sub"],
        balance=float(data["balance"]),
        image=data["image"],
        date=data["date"],)

    result = await session.execute(query)
    await session.commit()


async def orm_delete_user(session: AsyncSession , user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()