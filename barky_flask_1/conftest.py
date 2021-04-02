import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, DateTime
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


def wait_for_sqllite_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Sqllite DB never came up")


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
def sqllite_db():
    engine = create_engine(config.get_sqllite_uri())
    wait_for_sqllite_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(sqllite_db):
    start_mappers()
    yield sessionmaker(bind=sqllite_db)()
    clear_mappers()


@pytest.fixture
def add_bookmark(sqllite_session):


    def _add_bookmark():
        sqllite_session.execute(
            "INSERT INTO bookmark (title, url, notes) VALUES (?, ?, ?)"
            " VALUES ('test1', 'http://test1.com', 'test1 notes')",
        )
        [[bookmark_id]] = sqllite_session.execute(
            "SELECT id FROM bookmark WHERE url='http://test1.com' ",
        )
        sqllite_session.commit()

    yield _add_bookmark

    sqllite_session.execute(
        "DELETE FROM bookmark WHERE id=:bookmark_id"
    )
    sqllite_session.commit()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()