from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


class OutOfStock(Exception):
    pass

class StocknotMatch(Exception):
    pass

def add(catalog_item: CatalogItem, cart_item: List[CartItem]) -> str:
        for c in cart_item :
                if c.can_add(catalog_item) :
                    print('OutOfStock IN IF')
                    if c.sku_match(catalog_item) :
                            print('StocknotMatch IN IF')

                            cart_item.add(catalog_item)
                            return cart_item.reference
                    else:
                        print('StocknotMatch IN ELSE')
                        raise StocknotMatch(f"SKU does not match for sku {catalog_item.sku}")
                else:
                    raise OutOfStock(f"Out of stock for sku {catalog_item.sku}")
                    print('OutOfStock IN ELSE')



@dataclass(frozen=True)
class CatalogItem:
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
        self._items = set()  # type: Set[CatalogItem]

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

    def can_add(self, item: CatalogItem) -> bool:
        print(self.qty)
        print(item.maxAllowedPurchaseQty)
        print(self.qty >= item.maxAllowedPurchaseQty)

        return self.qty >= item.maxAllowedPurchaseQty

    def sku_match(self, item: CatalogItem) -> bool:
        return self.sku == item.sku 
