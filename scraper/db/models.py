from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from scraper.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    sku: Mapped[str | None] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(500))
    brand: Mapped[str | None] = mapped_column(String(200))
    category: Mapped[str | None] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    prices: Mapped[list["Price"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="Price.scraped_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} title={self.title!r}>"


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )

    value: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    in_stock: Mapped[bool] = mapped_column(default=True)

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    product: Mapped[Product] = relationship(back_populates="prices")

    __table_args__ = (
        Index("ix_prices_product_scraped", "product_id", "scraped_at"),
    )
    def __repr__(self) -> str:
        return f"<Price {self.value} {self.currency} at {self.scraped_at}>"
