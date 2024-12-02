from sqlalchemy import select, delete, update
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User

async def orm_add_user(session: AsyncSession , data: dict):
    obj = User(
        id = data["id"],
        name = data["name"],
        status_subscription = data["status_sub"],
        balance = data["balance"],
        image = data["image"],
        date = data["date"],
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
        name = data["name"],
        status_subscription = data["status_sub"],
        balance = float(data["balance"]),
        image = data["image"],
        date = data["date"],)

    result = await session.execute(query)
    await session.commit()

async def orm_update_user_balance(session:AsyncSession, user_id: int, balance: float):
    query = update(User).where(User.id == user_id).values(balance = balance)
    result = await session.execute(query)
    await session.commit()

async def orm_update_user_image(session:AsyncSession, user_id: int, image_id: str):
    query = update(User).where(User.id == user_id).values(image = image_id)
    result = await session.execute(query)
    await session.commit()

async def orm_delete_user(session: AsyncSession , user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()