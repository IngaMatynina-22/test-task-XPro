from decimal import Decimal

from sqlalchemy import ForeignKey, Float, Numeric, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    seo_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)

    meta_title: Mapped[str | None] = mapped_column("meta_titile", String(255), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)

    image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 1 - enabled, 0 - disabled
    status: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    manufacturer_id: Mapped[int | None] = mapped_column(nullable=True)

    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    viewed: Mapped[int] = mapped_column(default=0, nullable=False)

    categories: Mapped[list["ProductCategory"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    attributes: Mapped[list["ProductAttribute"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductCategory(Base):
    __tablename__ = "product_category"
    __table_args__ = (
        UniqueConstraint("product_id", "category_id", name="product_category_product_id_category_id_key"),
    )

    product_category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship(back_populates="categories")


class ProductImage(Base):
    __tablename__ = "product_image"

    product_image_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    image: Mapped[str] = mapped_column(String(500), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="images")


class ProductAttribute(Base):
    __tablename__ = "product_attribute"

    product_attribute_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    group_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="attributes")