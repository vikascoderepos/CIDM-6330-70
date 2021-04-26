from __future__ import annotations

import model
from model import CartItem
from repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, products):
    return sku in {p.sku for p in products}


def add(item: CartItem, repo: AbstractRepository, session) -> str:
    products = repo.list()
    if not is_valid_sku(item.sku, products):
        raise InvalidSku(f"Invalid sku {item.sku}")
    productref = model.add(item, products)
    session.commit()
    return productref