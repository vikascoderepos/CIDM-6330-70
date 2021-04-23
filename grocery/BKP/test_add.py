from datetime import date, timedelta
import pytest
from model import add, Product, CartItem, OutOfStock, StocknotMatch

# cart_item = CartItem("item1", "SMALL-FORK", 10)
# add(Product("SMALL-FORK", "SMALL FORK1", 11, 'SOME BRAND2' , 2), [cart_item])

def test_raises_out_of_stock_exception_if_cannot_add():
    cart_item = CartItem("item1", "SMALL-FORK", 10)
    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        add(Product("SMALL-FORK1", "SMALL FORK", 11, 'SOME BRAND2' , 2), [cart_item])


def test_raises_sku_do_not_match_exception_if_cannot_add():
    cart_item = CartItem("item1", "SMALL-FORK", 10)

    with pytest.raises(StocknotMatch, match="SMALL-FORK"):
        add(Product("SMALL-FORK1", "SMALL FORK", 1, 'SOME BRAND2' , 2), [cart_item])


