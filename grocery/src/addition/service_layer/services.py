from __future__ import annotations
from typing import Optional

from addition.domain import model
from addition.domain.model import CartItem
from addition.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, products):
    return sku in {p.sku for p in products}


def add_product(ref: str, sku: str, qty : int , maxAllowedPurchaseQty: int, brand: str, price: float, uow: unit_of_work.AbstractUnitOfWork,):
    with uow:
        cart = uow.carts.get(sku=sku)
        if cart is None:
            cart = model.Cart(sku, products=[])
            uow.carts.add(cart)

        cart.products.append(model.Product(ref, sku, qty, maxAllowedPurchaseQty, brand, price ))
        uow.commit()

def add(itemid: str, sku: str, qty: int,uow: unit_of_work.AbstractUnitOfWork) -> str:
    item = CartItem(itemid, sku, qty)
    with uow:
        print(sku)

        cart = uow.carts.get(sku=item.sku)
        print('IN GET')
        print(cart)
        if cart is None:
            raise InvalidSku(f"Invalid sku {item.sku}")
        productref = cart.add(item)
        uow.commit()
    return productref