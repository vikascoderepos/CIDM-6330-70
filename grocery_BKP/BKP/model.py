from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


class OutOfStock(Exception):
    pass

class StocknotMatch(Exception):
    pass

def add(product: Product, cart_item: List[CartItem]) -> str:
        for c in cart_item :
                if c.can_add(product) :
                    if c.sku_match(product) :

                            c.add(product)

                            print(c.reference)
                            return c.reference
                    else:
                        raise StocknotMatch(f"SKU does not match for sku {product.sku}")
                else:
                    raise OutOfStock(f"Out of stock for sku {product.sku}")



@dataclass(frozen=True)
class Product:
    sku : str
    name : str
    maxAllowedPurchaseQty : int 
    brand : str
    price : float


class CartItem:
    def __init__(self, ref: str, sku: str, qty: int):
        self.reference = ref
        self.sku = sku
        self.qty = qty
        self._items = set()  # type: Set[Product]

    def __repr__(self):
        return f"<CartItem {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, CartItem):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def add(self, item: CatalogItem):
        if self.can_add(item):
            self._items.add(item)

    def delete(self, item: CatalogItem):
        if item in self._items:
            self._items.remove(item)

    @property
    def total_quantity(self) -> int:
        return sum(item.qty for line in self._items)

    def can_add(self, item: Product) -> bool:
        return self.qty >= item.maxAllowedPurchaseQty

    def sku_match(self, item: Product) -> bool:
        return self.sku == item.sku 
