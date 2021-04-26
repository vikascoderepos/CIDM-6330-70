from addition.domain.model import  Product, CartItem


def test_adding_to_a_product_reduces_the_available_quantity():
    product = Product("oref", "WHEAT-1-GALLON", 10, 5, 'CHAKRI ATTA' , 16)
    item = CartItem("iref", "WHEAT-1-GALLON", 2)
    product.add(item)
    assert product.available_quantity == 8


def make_product_and_item(sku, product_qty, product_max_allowed_qty, product_brand, product_price, item_qty):
    return (
        Product("product-001", sku, product_qty, product_max_allowed_qty, product_brand, product_price ),
        CartItem("item-123", sku, item_qty),
    )

def test_can_add_if_available_greater_than_required():
    large_product, small_item = make_product_and_item("WHEAT-1-GALLON", 20, 20, 'CHAKRI ATTA' , 16 ,10)
    assert large_product.can_add(small_item)

def test_cannot_add_if_available_smaller_than_required():
    small_product, large_item = make_product_and_item("WHEAT-1-GALLON", 5, 5, 'CHAKRI ATTA' , 16 ,10)
    assert small_product.can_add(large_item) is False

def test_can_add_if_available_equal_to_required():
    product, item = make_product_and_item("WHEAT-1-GALLON", 5, 5, 'CHAKRI ATTA' , 16 ,5)
    assert product.can_add(item)

def test_cannot_add_if_skus_do_not_match():
    product = Product("product-001", "WHEAT-1-GALLON", 10, 5, 'CHAKRI ATTA' , 16)
    different_sku_item = CartItem("item-123", "RICE-1-GALLON", 2)
    assert product.can_add(different_sku_item) is False


def test_add_is_idempotent():
    product, item = make_product_and_item("WHEAT-1-GALLON", 20, 20, 'CHAKRI ATTA' , 16 ,2)
    product.add(item)
    product.add(item)
    assert product.available_quantity == 18


def test_delete():
    product, item = make_product_and_item("WHEAT-1-GALLON", 20, 20, 'CHAKRI ATTA' , 16 ,1)
    product.add(item)
    product.delete(item)
    assert product.available_quantity == 20


def test_can_only_delete_added_items():
    product, undeleted_item  = make_product_and_item("WHEAT-1-GALLON", 20, 20, 'CHAKRI ATTA' , 16 ,1)
    product.delete(undeleted_item)
    assert product.available_quantity == 20