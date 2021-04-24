import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from orm import metadata, start_mappers
import config


@pytest.fixture
def in_memory_db():
    engine=create_engine('sqlite://',echo=True)
    metadata.create_all(engine)
    return engine



@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()

def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    return engine.connect()
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_item(postgres_session):
    products_added = set()
    skus_added = set()

    def _add_item(items):
        for ref, sku, qty, max_allowed, brand, price  in items:
            postgres_session.execute(
                "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price)"
                " VALUES (:ref, :sku, :qty, :max_allowed, :brand, :price)",
                dict(ref=ref, sku=sku, qty=qty, max_allowed=max_allowed, brand=brand, price=price),
            )
            [[product_id]] = postgres_session.execute(
                "SELECT id FROM products WHERE reference=:ref AND sku=:sku",
                dict(ref=ref, sku=sku),
            )
            products_added.add(product_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_item

    for product_id in products_added:
        postgres_session.execute(
            "DELETE FROM items WHERE product_id=:product_id",
            dict(product_id=product_id),
        )
        postgres_session.execute(
            "DELETE FROM products WHERE id=:product_id", dict(product_id=product_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            "DELETE FROM cart_items WHERE sku=:sku", dict(sku=sku),
        )
        postgres_session.commit()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()