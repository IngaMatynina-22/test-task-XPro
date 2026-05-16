from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.models import Base

# Important: import models so SQLAlchemy registers tables
from src.category import models as category_models  # noqa: F401
from src.product import models as product_models  # noqa: F401

import asyncio

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    retries = 10

    for attempt in range(retries):
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            print("Database initialized")
            return

        except Exception as error:
            print(f"Database connection failed: {error}")

            if attempt == retries - 1:
                raise

            await asyncio.sleep(3)