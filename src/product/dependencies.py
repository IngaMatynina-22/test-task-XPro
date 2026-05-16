from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.product import service
from src.product.exceptions import (
    ProductAttributeNotFound,
    ProductCategoryNotFound,
    ProductImageNotFound,
    ProductNotFound,
)
from src.product.models import Product, ProductAttribute, ProductCategory, ProductImage


async def valid_product_id(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Product:
    product = await service.get_product_by_id(db, product_id)

    if product is None:
        raise ProductNotFound(product_id)

    return product


async def valid_product_image_id(
    product_image_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductImage:
    image = await service.get_product_image_by_id(db, product_image_id)

    if image is None:
        raise ProductImageNotFound(product_image_id)

    return image


async def valid_product_category_id(
    product_category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCategory:
    product_category = await service.get_product_category_by_id(db, product_category_id)

    if product_category is None:
        raise ProductCategoryNotFound(product_category_id)

    return product_category


async def valid_product_attribute_id(
    product_attribute_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductAttribute:
    attribute = await service.get_product_attribute_by_id(db, product_attribute_id)

    if attribute is None:
        raise ProductAttributeNotFound(product_attribute_id)

    return attribute