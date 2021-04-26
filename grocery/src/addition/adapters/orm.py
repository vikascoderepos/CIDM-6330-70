from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Float,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from addition.domain import model


metadata = MetaData()

cart_items = Table(
    "cart_items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("itemid", String(255)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("maxAllowedPurchaseQty", Integer, nullable=False),
    Column("brand", String(255)),
    Column("price", Float),
)

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cartitem_id", ForeignKey("cart_items.id")),
    Column("product_id", ForeignKey("products.id")),
)


def start_mappers():
    items_mapper = mapper(model.CartItem, cart_items)
    mapper(
        model.Product,
        products,
        properties={
            "_items": relationship(
                items_mapper, secondary=items, collection_class=set,
            )
        },
    )