from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.dependencies import valid_category_id
from src.category.models import Category
from src.category.schemas import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategorySortField,
    CategoryUpdate,
    SortDirection,
)
from src.category import service
from src.database import get_db


router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.get(
    "",
    response_model=CategoryListResponse,
    summary="Get category list",
    description=(
        "Returns paginated category list. "
        "Each category name contains the full category path, "
        "for example: `Для мотоцикліста > Аксесуари > Рюкзаки`."
    ),
)
async def get_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100, description="Number of items to return.")] = 20,
    offset: Annotated[int, Query(ge=0, description="Number of items to skip.")] = 0,
    search: Annotated[
        str | None,
        Query(description="Search by category ID or category name."),
    ] = None,
    status_filter: Annotated[
        int | None,
        Query(alias="status", ge=0, le=1, description="Filter by status: 1 - enabled, 0 - disabled."),
    ] = None,
    sort_by: Annotated[
        CategorySortField,
        Query(description="Field used for sorting."),
    ] = CategorySortField.NAME,
    sort_direction: Annotated[
        SortDirection,
        Query(description="Sort direction: asc or desc."),
    ] = SortDirection.ASC,
) -> CategoryListResponse:
    return await service.get_categories(
        db,
        limit=limit,
        offset=offset,
        search=search,
        status=status_filter,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get category details",
    description="Returns all stored data for a single category by ID.",
)
async def get_category(
    category: Annotated[Category, Depends(valid_category_id)],
) -> Category:
    return category


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
    description=(
        "Creates a new category. "
        "`parent_category_id = 0` means that the category is a root category."
    ),
)
async def create_category(
    payload: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Category:
    return await service.create_category(db, payload)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update category",
    description=(
        "Updates category data. "
        "`category_id`, `date_added` and `date_modify` are not editable. "
        "`date_modify` is updated automatically."
    ),
)
async def update_category(
    payload: CategoryUpdate,
    category: Annotated[Category, Depends(valid_category_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Category:
    return await service.update_category(db, category, payload)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
    description=(
        "Deletes category by ID. "
        "Nested subcategories are deleted recursively via database cascade."
    ),
)
async def delete_category(
    category: Annotated[Category, Depends(valid_category_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete_category(db, category)