from __future__ import annotations
from typing import Optional

from addition.domain import model
from addition.domain.model import CartItem
from addition.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, products):
    return sku in {p.sku for p in products}


def add_product(
        ref: str, sku: str, qty : int , maxAllowedPurchaseQty: int, brand: str, price: float,
        uow  #: unit_of_work.AbstractUnitOfWork
):
    with uow:
        uow.products.add(model.Product(ref, sku, qty, maxAllowedPurchaseQty, brand, price ))
        uow.commit()


def add(
        itemid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    item = CartItem(itemid, sku, qty)
    with uow:
        products = uow.products.list()
        if not is_valid_sku(item.sku, products):
            raise InvalidSku(f'Invalid sku {item.sku}')
        productref = model.add(item, products)
        uow.commit()
    return productref
