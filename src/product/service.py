from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.models import Category
from src.category.utils import build_category_path
from src.product.models import (
    Product,
    ProductAttribute,
    ProductCategory,
    ProductImage,
)
from src.product.schemas import (
    ProductAttributeCreate,
    ProductAttributeUpdate,
    ProductCategoryCreate,
    ProductCategoryResponse,
    ProductCreate,
    ProductImageCreate,
    ProductImageUpdate,
    ProductListItem,
    ProductListResponse,
    ProductResponse,
    ProductSortField,
    ProductUpdate,
    SortDirection,
)


async def get_product_by_id(
    db: AsyncSession,
    product_id: int,
) -> Product | None:
    result = await db.execute(
        select(Product).where(Product.product_id == product_id)
    )
    return result.scalar_one_or_none()


async def get_product_image_by_id(
    db: AsyncSession,
    product_image_id: int,
) -> ProductImage | None:
    result = await db.execute(
        select(ProductImage).where(ProductImage.product_image_id == product_image_id)
    )
    return result.scalar_one_or_none()


async def get_product_category_by_id(
    db: AsyncSession,
    product_category_id: int,
) -> ProductCategory | None:
    result = await db.execute(
        select(ProductCategory).where(
            ProductCategory.product_category_id == product_category_id
        )
    )
    return result.scalar_one_or_none()


async def get_product_attribute_by_id(
    db: AsyncSession,
    product_attribute_id: int,
) -> ProductAttribute | None:
    result = await db.execute(
        select(ProductAttribute).where(
            ProductAttribute.product_attribute_id == product_attribute_id
        )
    )
    return result.scalar_one_or_none()


async def get_categories_by_id(db: AsyncSession) -> dict[int, Category]:
    result = await db.execute(select(Category))
    categories = list(result.scalars().all())

    return {
        category.category_id: category
        for category in categories
    }


async def build_product_response(
    db: AsyncSession,
    product: Product,
) -> ProductResponse:
    categories_by_id = await get_categories_by_id(db)

    category_result = await db.execute(
        select(ProductCategory).where(ProductCategory.product_id == product.product_id)
    )
    product_categories = list(category_result.scalars().all())

    image_result = await db.execute(
        select(ProductImage)
        .where(ProductImage.product_id == product.product_id)
        .order_by(ProductImage.sort_order.asc())
    )
    images = list(image_result.scalars().all())

    attribute_result = await db.execute(
        select(ProductAttribute)
        .where(ProductAttribute.product_id == product.product_id)
        .order_by(ProductAttribute.sort_order.asc())
    )
    attributes = list(attribute_result.scalars().all())

    categories = [
        ProductCategoryResponse(
            product_category_id=item.product_category_id,
            product_id=item.product_id,
            category_id=item.category_id,
            category_name=build_category_path(
                categories_by_id[item.category_id],
                categories_by_id,
            )
            if item.category_id in categories_by_id
            else "",
        )
        for item in product_categories
    ]

    return ProductResponse(
        product_id=product.product_id,
        name=product.name,
        description=product.description,
        seo_keyword=product.seo_keyword,
        meta_title=product.meta_title,
        meta_description=product.meta_description,
        meta_keyword=product.meta_keyword,
        image=product.image,
        status=product.status,
        price=product.price,
        model=product.model,
        manufacturer_id=product.manufacturer_id,
        rating=product.rating,
        viewed=product.viewed,
        date_added=product.date_added,
        date_modify=product.date_modify,
        categories=categories,
        images=images,
        attributes=attributes,
    )


async def get_products(
    db: AsyncSession,
    *,
    limit: int,
    offset: int,
    category_id: int | None,
    price_from: float | None,
    price_to: float | None,
    sort_by: ProductSortField,
    sort_direction: SortDirection,
) -> ProductListResponse:
    result = await db.execute(select(Product))
    products = list(result.scalars().all())

    categories_by_id = await get_categories_by_id(db)

    product_category_result = await db.execute(select(ProductCategory))
    product_categories = list(product_category_result.scalars().all())

    categories_by_product_id: dict[int, list[ProductCategory]] = {}

    for item in product_categories:
        categories_by_product_id.setdefault(item.product_id, []).append(item)

    items: list[ProductListItem] = []

    for product in products:
        linked_categories = categories_by_product_id.get(product.product_id, [])

        if category_id is not None:
            linked_category_ids = {
                item.category_id
                for item in linked_categories
            }

            if category_id not in linked_category_ids:
                continue

        if price_from is not None and product.price is not None and product.price < price_from:
            continue

        if price_to is not None and product.price is not None and product.price > price_to:
            continue

        first_category_name = None

        if linked_categories:
            first_category_id = linked_categories[0].category_id
            category = categories_by_id.get(first_category_id)

            if category is not None:
                first_category_name = build_category_path(category, categories_by_id)

        items.append(
            ProductListItem(
                product_id=product.product_id,
                name=product.name,
                category=first_category_name,
                price=product.price,
            )
        )

    reverse = sort_direction == SortDirection.DESC

    if sort_by == ProductSortField.PRICE:
        items.sort(
            key=lambda item: item.price if item.price is not None else 0,
            reverse=reverse,
        )
    elif sort_by == ProductSortField.CATEGORY:
        items.sort(
            key=lambda item: (item.category or "").lower(),
            reverse=reverse,
        )
    else:
        items.sort(
            key=lambda item: item.name.lower(),
            reverse=reverse,
        )

    total = len(items)

    return ProductListResponse(
        items=items[offset : offset + limit],
        total=total,
        limit=limit,
        offset=offset,
    )


async def create_product(
    db: AsyncSession,
    payload: ProductCreate,
) -> ProductResponse:
    product_data = payload.model_dump(
        exclude={
            "categories",
            "images",
            "attributes",
        }
    )

    product = Product(**product_data)

    db.add(product)
    await db.flush()

    for category in payload.categories:
        db.add(
            ProductCategory(
                product_id=product.product_id,
                category_id=category.category_id,
            )
        )

    for image in payload.images:
        db.add(
            ProductImage(
                product_id=product.product_id,
                **image.model_dump(),
            )
        )

    for attribute in payload.attributes:
        db.add(
            ProductAttribute(
                product_id=product.product_id,
                **attribute.model_dump(),
            )
        )

    await db.commit()
    await db.refresh(product)

    return await build_product_response(db, product)


async def update_product(
    db: AsyncSession,
    product: Product,
    payload: ProductUpdate,
) -> ProductResponse:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return await build_product_response(db, product)


async def delete_product(
    db: AsyncSession,
    product: Product,
) -> None:
    await db.delete(product)
    await db.commit()


async def get_product_images(
    db: AsyncSession,
    product_id: int,
) -> list[ProductImage]:
    result = await db.execute(
        select(ProductImage)
        .where(ProductImage.product_id == product_id)
        .order_by(ProductImage.sort_order.asc())
    )
    return list(result.scalars().all())


async def create_product_image(
    db: AsyncSession,
    product_id: int,
    payload: ProductImageCreate,
) -> ProductImage:
    image = ProductImage(
        product_id=product_id,
        **payload.model_dump(),
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    return image


async def update_product_image(
    db: AsyncSession,
    image: ProductImage,
    payload: ProductImageUpdate,
) -> ProductImage:
    image.sort_order = payload.sort_order

    await db.commit()
    await db.refresh(image)

    return image


async def delete_product_image(
    db: AsyncSession,
    image: ProductImage,
) -> None:
    await db.delete(image)
    await db.commit()


async def get_product_categories(
    db: AsyncSession,
    product_id: int,
) -> list[ProductCategoryResponse]:
    categories_by_id = await get_categories_by_id(db)

    result = await db.execute(
        select(ProductCategory).where(ProductCategory.product_id == product_id)
    )
    product_categories = list(result.scalars().all())

    return [
        ProductCategoryResponse(
            product_category_id=item.product_category_id,
            product_id=item.product_id,
            category_id=item.category_id,
            category_name=build_category_path(categories_by_id[item.category_id], categories_by_id)
            if item.category_id in categories_by_id
            else "",
        )
        for item in product_categories
    ]


async def create_product_category(
    db: AsyncSession,
    product_id: int,
    payload: ProductCategoryCreate,
) -> ProductCategoryResponse:
    product_category = ProductCategory(
        product_id=product_id,
        category_id=payload.category_id,
    )

    db.add(product_category)
    await db.commit()
    await db.refresh(product_category)

    categories_by_id = await get_categories_by_id(db)
    category = categories_by_id.get(product_category.category_id)

    return ProductCategoryResponse(
        product_category_id=product_category.product_category_id,
        product_id=product_category.product_id,
        category_id=product_category.category_id,
        category_name=build_category_path(category, categories_by_id) if category else "",
    )


async def delete_product_category(
    db: AsyncSession,
    product_category: ProductCategory,
) -> None:
    await db.delete(product_category)
    await db.commit()


async def get_product_attributes(
    db: AsyncSession,
    product_id: int,
) -> list[ProductAttribute]:
    result = await db.execute(
        select(ProductAttribute)
        .where(ProductAttribute.product_id == product_id)
        .order_by(ProductAttribute.sort_order.asc())
    )
    return list(result.scalars().all())


async def create_product_attribute(
    db: AsyncSession,
    product_id: int,
    payload: ProductAttributeCreate,
) -> ProductAttribute:
    attribute = ProductAttribute(
        product_id=product_id,
        **payload.model_dump(),
    )

    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)

    return attribute


async def update_product_attribute(
    db: AsyncSession,
    attribute: ProductAttribute,
    payload: ProductAttributeUpdate,
) -> ProductAttribute:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(attribute, field, value)

    await db.commit()
    await db.refresh(attribute)

    return attribute


async def delete_product_attribute(
    db: AsyncSession,
    attribute: ProductAttribute,
) -> None:
    await db.delete(attribute)
    await db.commit()
    
async def build_product_category_response(
    db: AsyncSession,
    product_category: ProductCategory,
) -> ProductCategoryResponse:
    categories_by_id = await get_categories_by_id(db)
    category = categories_by_id.get(product_category.category_id)

    return ProductCategoryResponse(
        product_category_id=product_category.product_category_id,
        product_id=product_category.product_id,
        category_id=product_category.category_id,
        category_name=build_category_path(category, categories_by_id) if category else "",
    )