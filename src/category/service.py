from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.models import Category
from src.category.schemas import (
    CategoryCreate,
    CategoryListItem,
    CategoryListResponse,
    CategorySortField,
    CategoryUpdate,
    SortDirection,
)
from src.category.utils import build_category_path, get_status_label


async def get_category_by_id(
    db: AsyncSession,
    category_id: int,
) -> Category | None:
    result = await db.execute(
        select(Category).where(Category.category_id == category_id)
    )
    return result.scalar_one_or_none()


async def get_categories(
    db: AsyncSession,
    *,
    limit: int,
    offset: int,
    search: str | None,
    status: int | None,
    sort_by: CategorySortField,
    sort_direction: SortDirection,
) -> CategoryListResponse:
    result = await db.execute(select(Category))
    all_categories = list(result.scalars().all())

    categories_by_id = {
        category.category_id: category
        for category in all_categories
    }

    items: list[CategoryListItem] = []

    for category in all_categories:
        full_path = build_category_path(category, categories_by_id)

        if search:
            search_lower = search.lower()
            is_id_match = search.isdigit() and category.category_id == int(search)
            is_name_match = search_lower in full_path.lower()

            if not is_id_match and not is_name_match:
                continue

        if status is not None and category.status != status:
            continue

        items.append(
            CategoryListItem(
                category_id=category.category_id,
                name=full_path,
                status=get_status_label(category.status),
            )
        )

    reverse = sort_direction == SortDirection.DESC

    if sort_by == CategorySortField.CATEGORY_ID:
        items.sort(key=lambda item: item.category_id, reverse=reverse)
    else:
        items.sort(key=lambda item: item.name.lower(), reverse=reverse)

    total = len(items)

    return CategoryListResponse(
        items=items[offset : offset + limit],
        total=total,
        limit=limit,
        offset=offset,
    )
async def create_category(
    db: AsyncSession,
    payload: CategoryCreate,
) -> Category:
    category = Category(**payload.model_dump())
    
    if (
        payload.parent_category_id is not None
        and payload.parent_category_id == category.category_id
    ):
        raise ValueError("Category cannot be its own parent.")

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def update_category(
    db: AsyncSession,
    category: Category,
    payload: CategoryUpdate,
) -> Category:
    update_data = payload.model_dump(exclude_unset=True)

    parent_category_id = update_data.get("parent_category_id")

    if parent_category_id == category.category_id:
        raise ValueError("Category cannot be its own parent.")

    for field, value in update_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)

    return category


async def get_child_category_ids(
    db: AsyncSession,
    category_id: int,
) -> list[int]:
    result = await db.execute(
        select(Category.category_id).where(Category.parent_category_id == category_id)
    )

    child_ids = list(result.scalars().all())
    all_ids = []

    for child_id in child_ids:
        all_ids.extend(await get_child_category_ids(db, child_id))
        all_ids.append(child_id)

    return all_ids


async def delete_category(
    db: AsyncSession,
    category: Category,
) -> None:
    await db.delete(category)
    await db.commit()