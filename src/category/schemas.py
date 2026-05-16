from datetime import datetime
from enum import IntEnum, StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CategoryStatus(IntEnum):
    DISABLED = 0
    ENABLED = 1


class CategorySortField(StrEnum):
    CATEGORY_ID = "category_id"
    NAME = "name"


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class CategoryBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["Рюкзаки"],
        description="Category name.",
    )
    description: str | None = Field(
        default=None,
        examples=["Категорія товарів для мотоциклістів."],
        description="Category description.",
    )
    parent_category_id: int | None = Field(
        default=None,
        examples=[None],
        description="Parent category ID. Leave empty for root category.",
    )
    seo_keyword: str | None = Field(
        default=None,
        max_length=255,
        examples=["rukzaky"],
        description="SEO-friendly category URL keyword.",
    )
    meta_title: str | None = Field(
        default=None,
        max_length=255,
        examples=["Рюкзаки для мотоциклістів"],
        description="Meta title for SEO.",
    )
    meta_description: str | None = Field(
        default=None,
        examples=["Купити рюкзаки для мотоциклістів."],
        description="Meta description for SEO.",
    )
    meta_keyword: str | None = Field(
        default=None,
        max_length=255,
        examples=["рюкзаки, мото, аксесуари"],
        description="Meta keywords for SEO.",
    )
    image: str | None = Field(
        default=None,
        max_length=500,
        examples=["/images/categories/backpacks.jpg"],
        description="Category image path or URL.",
    )
    status: CategoryStatus = Field(
        default=CategoryStatus.DISABLED,
        description="Category status: 1 - enabled, 0 - disabled.",
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    parent_category_id: int | None = Field(default=None, examples=[None])
    seo_keyword: str | None = Field(default=None, max_length=255)
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keyword: str | None = Field(default=None, max_length=255)
    image: str | None = Field(default=None, max_length=500)
    status: CategoryStatus | None = None


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    date_added: datetime
    date_modify: datetime | None = None


class CategoryListItem(BaseModel):
    category_id: int = Field(description="Category ID.")
    name: str = Field(
        description="Full category path.",
        examples=["Для мотоцикліста > Аксесуари > Рюкзаки"],
    )
    status: str = Field(
        description="Human-readable category status.",
        examples=["Включена"],
    )


class CategoryListResponse(BaseModel):
    items: list[CategoryListItem]
    total: int
    limit: int
    offset: int