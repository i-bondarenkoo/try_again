from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from db.settings import settings


# движок
engine = create_async_engine(
    url=settings.db_url,
    echo=settings.db_echo,
)

# фабрика сессий
AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


# функция-генератор для получения сессии
async def get_session():
    async with AsyncSession() as session:
        yield session
