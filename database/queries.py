from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .session import async_session_factory
from .models import User


async def create_user(telegram_id: int, username: str, settings: dict = None):
    async with async_session_factory() as session:
        new_user = User(
            telegram_id=telegram_id, 
            username=username,
            settings=settings or {"theme": "dark"}
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user) # Обновляем объект, чтобы получить id из БД
        return new_user
    # 2. READ (Найти юзера)
async def get_user_by_tid(telegram_id: int) -> User | None:
    async with async_session_factory() as session:
        # Аналог: db.user.findUnique({ where: { telegram_id } })
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

# 3. UPDATE (Обновить JSONB поле)
async def update_user_settings(telegram_id: int, new_settings: dict):
    async with async_session_factory() as session:
        # Аналог: db.user.update({ where: { telegram_id }, data: { settings: new_settings } })
        query = update(User).where(User.telegram_id == telegram_id).values(settings=new_settings)
        await session.execute(query)
        await session.commit()

# 4. DELETE (Удалить)
async def delete_user(telegram_id: int):
    async with async_session_factory() as session:
        query = delete(User).where(User.telegram_id == telegram_id)
        await session.execute(query)
        await session.commit()