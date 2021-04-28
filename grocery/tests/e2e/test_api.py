import pytest
import requests

from addition import config
from ..random_refs import random_sku, random_productref, random_itemid

def post_to_add_product(ref, sku, qty, maxAllowedPurchaseQty, brand, price):
    url = config.get_api_url()
    r = requests.post(
        f"{url}/add_product", json={"ref": ref, "sku": sku, "qty": qty, "maxAllowedPurchaseQty": maxAllowedPurchaseQty, "brand": brand, "price": price}
    )
    assert r.status_code == 201

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_added_product():
    sku, othersku = random_sku(), random_sku("other")
    large_qty_product = random_productref(1)
    small_qty_product = random_productref(2)
    post_to_add_product(large_qty_product, sku, 20, 20, 'CHAKRI ATTA' , 16)
    post_to_add_product(small_qty_product, sku,  5, 5, 'CHAKRI ATTA' , 16)
    data = {"itemid": random_itemid(), "sku": sku, "qty": 6}
    
    url = config.get_api_url()
    r = requests.post(f"{url}/add", json=data)

    assert r.status_code == 201
    assert r.json()["productref"] == large_qty_product


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, itemid = random_sku(), random_itemid()
    data = {"itemid": itemid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/add", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"