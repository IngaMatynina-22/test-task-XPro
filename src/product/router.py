from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.product import service
from src.product.dependencies import (
    valid_product_attribute_id,
    valid_product_category_id,
    valid_product_id,
    valid_product_image_id,
)
from src.product.models import Product, ProductAttribute, ProductCategory, ProductImage
from src.product.schemas import (
    ProductAttributeCreate,
    ProductAttributeResponse,
    ProductAttributeUpdate,
    ProductCategoryCreate,
    ProductCategoryResponse,
    ProductCreate,
    ProductImageCreate,
    ProductImageResponse,
    ProductImageUpdate,
    ProductListResponse,
    ProductResponse,
    ProductSortField,
    ProductUpdate,
    SortDirection,
)

from src.product.exceptions import ProductCategoryNotFound

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Get product list",
    description=(
        "Returns paginated product list with product ID, name, first linked category full path and price. "
        "Supports filtering by category and price range, sorting by name, price or category."
    ),
)
async def get_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100, description="Number of items to return.")] = 20,
    offset: Annotated[int, Query(ge=0, description="Number of items to skip.")] = 0,
    category_id: Annotated[int | None, Query(gt=0, description="Filter by linked category ID.")] = None,
    price_from: Annotated[float | None, Query(ge=0, description="Minimum product price.")] = None,
    price_to: Annotated[float | None, Query(ge=0, description="Maximum product price.")] = None,
    sort_by: Annotated[ProductSortField, Query(description="Field used for sorting.")] = ProductSortField.NAME,
    sort_direction: Annotated[SortDirection, Query(description="Sort direction.")] = SortDirection.ASC,
) -> ProductListResponse:
    return await service.get_products(
        db,
        limit=limit,
        offset=offset,
        category_id=category_id,
        price_from=price_from,
        price_to=price_to,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product details",
    description=(
        "Returns all product fields, linked categories with full category names, "
        "additional images and product attributes."
    ),
)
async def get_product(
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductResponse:
    return await service.build_product_response(db, product)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description=(
        "Creates a product. Required field: name. "
        "Status is disabled by default. Categories, images and attributes can be passed during creation."
    ),
)
async def create_product(
    payload: ProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductResponse:
    return await service.create_product(db, payload)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description=(
        "Updates product fields. product_id, date_added and date_modify are not editable. "
        "date_modify is updated automatically."
    ),
)
async def update_product(
    payload: ProductUpdate,
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductResponse:
    return await service.update_product(db, product, payload)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Deletes product and all related category links, images and attributes.",
)
async def delete_product(
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete_product(db, product)


@router.get(
    "/{product_id}/image",
    response_model=list[ProductImageResponse],
    summary="Get product images",
    description="Returns all additional product images ordered by sort_order.",
)
async def get_product_images(
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProductImage]:
    return await service.get_product_images(db, product.product_id)


@router.get(
    "/{product_id}/image/{product_image_id}",
    response_model=ProductImageResponse,
    summary="Get product image",
    description="Returns one additional product image by image ID.",
)
async def get_product_image(
    product: Annotated[Product, Depends(valid_product_id)],
    image: Annotated[ProductImage, Depends(valid_product_image_id)],
) -> ProductImage:
    return image


@router.post(
    "/{product_id}/image",
    response_model=ProductImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add product image",
    description="Adds an additional image to product.",
)
async def create_product_image(
    payload: ProductImageCreate,
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductImage:
    return await service.create_product_image(db, product.product_id, payload)


@router.patch(
    "/{product_id}/image/{product_image_id}",
    response_model=ProductImageResponse,
    summary="Update product image",
    description="Updates product image sort_order.",
)
async def update_product_image(
    payload: ProductImageUpdate,
    product: Annotated[Product, Depends(valid_product_id)],
    image: Annotated[ProductImage, Depends(valid_product_image_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductImage:
    return await service.update_product_image(db, image, payload)


@router.delete(
    "/{product_id}/image/{product_image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product image",
    description="Deletes additional product image.",
)
async def delete_product_image(
    product: Annotated[Product, Depends(valid_product_id)],
    image: Annotated[ProductImage, Depends(valid_product_image_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete_product_image(db, image)


@router.get(
    "/{product_id}/category",
    response_model=list[ProductCategoryResponse],
    summary="Get product categories",
    description="Returns all categories linked to product with full category paths.",
)
async def get_product_categories(
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProductCategoryResponse]:
    return await service.get_product_categories(db, product.product_id)


@router.get(
    "/{product_id}/category/{product_category_id}",
    response_model=ProductCategoryResponse,
    summary="Get product category link",
    description="Returns one product-category link with full category path.",
)
async def get_product_category(
    product: Annotated[Product, Depends(valid_product_id)],
    product_category: Annotated[ProductCategory, Depends(valid_product_category_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCategoryResponse:
    return await service.build_product_category_response(db, product_category)

@router.post(
    "/{product_id}/category",
    response_model=ProductCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add product category",
    description="Links product to category.",
)
async def create_product_category(
    payload: ProductCategoryCreate,
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCategoryResponse:
    return await service.create_product_category(db, product.product_id, payload)


@router.delete(
    "/{product_id}/category/{product_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product category link",
    description="Deletes product-category link.",
)
async def delete_product_category(
    product: Annotated[Product, Depends(valid_product_id)],
    product_category: Annotated[ProductCategory, Depends(valid_product_category_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete_product_category(db, product_category)


@router.get(
    "/{product_id}/attribute",
    response_model=list[ProductAttributeResponse],
    summary="Get product attributes",
    description="Returns all product attributes ordered by sort_order.",
)
async def get_product_attributes(
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProductAttribute]:
    return await service.get_product_attributes(db, product.product_id)


@router.get(
    "/{product_id}/attribute/{product_attribute_id}",
    response_model=ProductAttributeResponse,
    summary="Get product attribute",
    description="Returns one product attribute by ID.",
)
async def get_product_attribute(
    product: Annotated[Product, Depends(valid_product_id)],
    attribute: Annotated[ProductAttribute, Depends(valid_product_attribute_id)],
) -> ProductAttribute:
    return attribute


@router.post(
    "/{product_id}/attribute",
    response_model=ProductAttributeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add product attribute",
    description="Adds product attribute.",
)
async def create_product_attribute(
    payload: ProductAttributeCreate,
    product: Annotated[Product, Depends(valid_product_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductAttribute:
    return await service.create_product_attribute(db, product.product_id, payload)


@router.patch(
    "/{product_id}/attribute/{product_attribute_id}",
    response_model=ProductAttributeResponse,
    summary="Update product attribute",
    description="Updates product attribute. product_attribute_id and product_id are not editable.",
)
async def update_product_attribute(
    payload: ProductAttributeUpdate,
    product: Annotated[Product, Depends(valid_product_id)],
    attribute: Annotated[ProductAttribute, Depends(valid_product_attribute_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductAttribute:
    return await service.update_product_attribute(db, attribute, payload)


@router.delete(
    "/{product_id}/attribute/{product_attribute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product attribute",
    description="Deletes product attribute.",
)
async def delete_product_attribute(
    product: Annotated[Product, Depends(valid_product_id)],
    attribute: Annotated[ProductAttribute, Depends(valid_product_attribute_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete_product_attribute(db, attribute)