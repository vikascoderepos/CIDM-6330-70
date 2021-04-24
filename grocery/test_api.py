import uuid
import pytest
import requests

import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_productref(name=""):
    return f"product-{name}-{random_suffix()}"


def random_itemid(name=""):
    return f"item-{name}-{random_suffix()}"


@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_added_product(add_item):
    sku, othersku = random_sku(), random_sku("other")
    large_qty_product = random_productref(1)
    small_qty_product = random_productref(2)
    add_item(
        [
            (large_qty_product, sku, 20, 20, 'CHAKRI ATTA' , 16 ),
            (small_qty_product, sku, 5, 5, 'CHAKRI ATTA' , 16 ),
        ]
    )
    data = {"itemid": random_itemid(), "sku": sku, "qty": 6}
    url = config.get_api_url()

    r = requests.post(f"{url}/add", json=data)
    print(r)
    assert r.status_code == 201
    assert r.json()["productref"] == large_qty_product


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, itemid = random_sku(), random_itemid()
    data = {"itemid": itemid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/add", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"