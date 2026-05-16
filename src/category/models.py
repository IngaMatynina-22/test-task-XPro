from sqlalchemy import ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", ondelete="CASCADE"),
        default=None,
        nullable=True,
        index=True,
    )

    seo_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # In task typo is "meta_titile", keep DB column compatible but use clean Python name.
    meta_title: Mapped[str | None] = mapped_column("meta_titile", String(255), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)

    image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 1 - enabled, 0 - disabled
    status: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    children: Mapped[list["Category"]] = relationship(
    "Category",
    back_populates="parent",
    cascade="all, delete-orphan",
    passive_deletes=True,
)

    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side=[category_id],
        back_populates="children",
    )