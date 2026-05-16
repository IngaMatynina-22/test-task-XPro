from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.exceptions import CategoryNotFound
from src.category.models import Category
from src.category.service import get_category_by_id
from src.database import get_db


async def valid_category_id(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Category:
    category = await get_category_by_id(db, category_id)

    if category is None:
        raise CategoryNotFound(category_id)

    return category