from datetime import date, timedelta
import pytest
from addition.domain.model import Cart, CartItem, Product, OutOfStock



def test_prefers_more_maxAllowedPurchaseQty_products():
    more_maxAllowed_product = Product("pref", "RICE-1-GALLON", 11, 5, 'SONA MASURI' , 2)
    less_maxAllowed_product = Product("pref", "RICE-1-GALLON", 3, 1, 'NIRAPARA' , 2)

    cart = Cart(sku="RICE-1-GALLON", products=[more_maxAllowed_product, less_maxAllowed_product])
    item = CartItem("iref", "RICE-1-GALLON", 4)
    cart.add(item)

    assert more_maxAllowed_product.available_quantity == 7
    assert less_maxAllowed_product.available_quantity == 3


def test_prefers_more_qty_products():
    more_quantity_product = Product("pref", "RICE-1-GALLON", 11, 5, 'SONA MASURI' , 2)
    less_quantity_product = Product("pref", "RICE-1-GALLON", 3, 3, 'NIRAPARA' , 2)
    cart = Cart(sku="RICE-1-GALLON", products=[more_quantity_product, less_quantity_product])
    item = CartItem("iref", "RICE-1-GALLON", 4)

    cart.add(item)

    assert more_quantity_product.available_quantity == 7
    assert less_quantity_product.available_quantity == 3


def test_returns_added_product_ref():
    more_quantity_product = Product("pref", "RICE-1-GALLON", 11, 5, 'SONA MASURI' , 2)
    less_quantity_product = Product("pref", "RICE-1-GALLON", 3, 3, 'NIRAPARA' , 2)
    item = CartItem("iref", "RICE-1-GALLON", 4)
    cart = Cart(sku="RICE-1-GALLON", products=[more_quantity_product, less_quantity_product])
    adds = cart.add(item)
    assert adds == more_quantity_product.reference


def test_raises_out_of_stock_exception_if_cannot_add():
    product = Product("pref", "WHEAT-1-GALLON", 11, 11, 'CHAKRI ATTA' , 2)
    cart = Cart(sku="WHEAT-1-GALLON", products=[product])
    cart.add(CartItem("item1", "WHEAT-1-GALLON", 11))

    with pytest.raises(OutOfStock, match="WHEAT-1-GALLON"):
        cart.add(CartItem("item2", "WHEAT-1-GALLON", 1))

def test_increments_version_number():
    item = CartItem("iref", "RICE-1-GALLON", 4)
    cart = Cart(
        sku="RICE-1-GALLON", products=[Product("p1", "RICE-1-GALLON", 10, 11, 'SONAMASURI RICE' , 2)]
    )
    cart.version_number = 7
    cart.add(item)
    assert cart.version_number == 8