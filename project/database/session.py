import os 
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
load_dotenv()

# DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost:5432/my_db"
# DATABASE_URL=postgres://admin:admin@localhost:5432/node_app?schema=public
DATABASE_URL = os.getenv("DATABASE_URL")

IS_DEBUG = os.getenv("DEBUG", "False").lower() == "true"

if not DATABASE_URL:
  raise ValueError("❌ DATABASE_URL не найден! Создай файл .env и добавь туда DATABASE_URL=...")

engine = create_async_engine(
    DATABASE_URL,
    echo=IS_DEBUG,
    pool_size=5,
    max_overflow=10
)

async_session_factory = async_sessionmaker(
        engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

