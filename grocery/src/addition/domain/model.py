from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


class OutOfStock(Exception):
    pass

class StocknotMatch(Exception):
    pass

def add(item: CartItem , products: List[Product]) -> str:
    try:
        product = next(p for p in sorted(products) if p.can_add(item))
        product.add(item)
        return product.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {item.sku}")


#@dataclass(frozen=True)
@dataclass(unsafe_hash=True)

class CartItem:
    itemid: str
    sku : str
    qty : int


class Product:
    def __init__(self, ref: str, sku: str, qty : int , maxAllowedPurchaseQty: int, brand: str, price: float):
        self.reference = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.maxAllowedPurchaseQty = maxAllowedPurchaseQty
        self.brand = brand
        self.price = price
        self._items = set()  # type: Set[CartItem]

    def __repr__(self):
        return f"<Product {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
    
    def __gt__(self, other):
        if self._purchased_quantity is None:
            return False
        if other._purchased_quantity is None:
            return True
        return self._purchased_quantity > other._purchased_quantity

    def add(self, item: CartItem):
        if self.can_add(item):
            self._items.add(item)

    def delete(self, item: CartItem):
        if item in self._items:
            self._items.remove(item)


    @property
    def added_quantity(self) -> int:
        for i in self._items:
            print(i)
        # print(sum(item.qty for item in self._items))
        return sum(item.qty for item in self._items)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.added_quantity

    def can_add(self, item: CartItem) -> bool:
        return self.maxAllowedPurchaseQty >= item.qty and self.available_quantity >= item.qty and self.sku == item.sku 

    def sku_match(self, item: CartItem) -> bool:
        return self.sku == item.sku 
