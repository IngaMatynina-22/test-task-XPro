from datetime import datetime
from decimal import Decimal
from enum import IntEnum, StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ProductStatus(IntEnum):
    DISABLED = 0
    ENABLED = 1


class ProductSortField(StrEnum):
    NAME = "name"
    PRICE = "price"
    CATEGORY = "category"


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class ProductImageCreate(BaseModel):
    image: str = Field(
        max_length=500,
        examples=["/images/products/image-1.jpg"],
        description="Product image path or URL.",
    )
    sort_order: int = Field(
        default=0,
        ge=0,
        description="Image sorting order.",
    )


class ProductImageUpdate(BaseModel):
    sort_order: int = Field(
        ge=0,
        description="Image sorting order.",
    )


class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_image_id: int
    product_id: int
    image: str
    sort_order: int


class ProductCategoryCreate(BaseModel):
    category_id: int = Field(
        gt=0,
        examples=[1],
        description="Category ID linked to product.",
    )


class ProductCategoryResponse(BaseModel):
    product_category_id: int
    product_id: int
    category_id: int
    category_name: str = Field(
        examples=["Для мотоцикліста > Аксесуари > Рюкзаки"],
        description="Full category path.",
    )


class ProductAttributeCreate(BaseModel):
    group_name: str | None = Field(
        default=None,
        max_length=255,
        examples=["Основні характеристики"],
    )
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["Матеріал"],
    )
    value: str | None = Field(
        default=None,
        examples=["Поліестер"],
    )
    sort_order: int = Field(
        default=0,
        ge=0,
    )


class ProductAttributeUpdate(BaseModel):
    group_name: str | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    value: str | None = None
    sort_order: int | None = Field(default=None, ge=0)


class ProductAttributeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_attribute_id: int
    product_id: int
    group_name: str | None
    name: str
    value: str | None
    sort_order: int


class ProductBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["Мотошолом LS2"],
        description="Product name.",
    )
    description: str | None = Field(
        default=None,
        examples=["Опис товару."],
        description="Product description.",
    )
    seo_keyword: str | None = Field(
        default=None,
        max_length=255,
        examples=["motosholom-ls2"],
    )
    meta_title: str | None = Field(
        default=None,
        max_length=255,
        examples=["Мотошолом LS2 купити"],
    )
    meta_description: str | None = Field(
        default=None,
        examples=["Купити мотошолом LS2."],
    )
    meta_keyword: str | None = Field(
        default=None,
        max_length=255,
        examples=["шолом, мото, ls2"],
    )
    image: str | None = Field(
        default=None,
        max_length=500,
        examples=["/images/products/helmet.jpg"],
    )
    status: ProductStatus = Field(
        default=ProductStatus.DISABLED,
        description="Product status: 1 - enabled, 0 - disabled.",
    )
    price: Decimal | None = Field(
        default=None,
        ge=0,
        examples=["3499.99"],
    )
    model: str | None = Field(
        default=None,
        max_length=255,
        examples=["LS2-FF800"],
    )
    manufacturer_id: int | None = Field(
        default=None,
        description="Manufacturer ID from external/source system. Manufacturer table is not provided in task.",
    )
    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )
    viewed: int = Field(
        default=0,
        ge=0,
    )


class ProductCreate(ProductBase):
    categories: list[ProductCategoryCreate] = Field(default_factory=list)
    images: list[ProductImageCreate] = Field(default_factory=list)
    attributes: list[ProductAttributeCreate] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    seo_keyword: str | None = Field(default=None, max_length=255)
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keyword: str | None = Field(default=None, max_length=255)
    image: str | None = Field(default=None, max_length=500)
    status: ProductStatus | None = None
    price: Decimal | None = Field(default=None, ge=0)
    model: str | None = Field(default=None, max_length=255)
    manufacturer_id: int | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    viewed: int | None = Field(default=None, ge=0)


class ProductListItem(BaseModel):
    product_id: int
    name: str
    category: str | None = Field(
        default=None,
        description="First linked product category full path.",
        examples=["Для мотоцикліста > Аксесуари > Рюкзаки"],
    )
    price: Decimal | None


class ProductListResponse(BaseModel):
    items: list[ProductListItem]
    total: int
    limit: int
    offset: int


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    date_added: datetime
    date_modify: datetime | None = None

    categories: list[ProductCategoryResponse] = Field(default_factory=list)
    images: list[ProductImageResponse] = Field(default_factory=list)
    attributes: list[ProductAttributeResponse] = Field(default_factory=list)