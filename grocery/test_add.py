from datetime import date, timedelta
import pytest
from model import add, Product, CartItem, OutOfStock, StocknotMatch



def test_returns_added_product_ref():
    more_quantity_product = Product("pref", "RICE-1-GALLON", 11, 5, 'SONA MASURI' , 2)
    less_quantity_product = Product("pref", "RICE-1-GALLON", 3, 3, 'NIRAPARA' , 2)
    item = CartItem("iref", "RICE-1-GALLON", 4)
    adds = add(item, [more_quantity_product,less_quantity_product])
    assert adds == more_quantity_product.reference


def test_raises_out_of_stock_exception_if_cannot_add():
    product = Product("pref", "WHEAT-1-GALLON", 11, 11, 'CHAKRI ATTA' , 2)
    add(CartItem("iref", "WHEAT-1-GALLON", 11), [product])
    with pytest.raises(OutOfStock, match="WHEAT-1-GALLON"):
        add(CartItem("iref", "WHEAT-1-GALLON", 1), [product])

