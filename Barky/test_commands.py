from commands import *
from datetime import datetime
import sys
import requests
import sqlite3
from datetime import datetime
import pytest

"""
  Setting some global vaiables which will be used for all tests
"""

now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y%H%M%S")
v_table_name = 'bookmarks'
pytest.db_file = "bookmarks.db"
pytest.table_name = v_table_name
pytest.date_time = date_time
pytest.v_title = "##########Test Data#################" + pytest.date_time
pytest.v_date =  now.strftime('%Y-%m-%d %H:%M:%S')
pytest.db = DatabaseManager(pytest.db_file)



""""
Test if CreateBookmarksTableCommand is successful
"""

def test_create_bookmarks_table_command() -> None:
    a = CreateBookmarksTableCommand()
    a.execute()
    query = "SELECT 1 FROM sqlite_master WHERE type='table' and name = 'bookmarks'"
    assert pytest.db._execute(query).fetchone() is not None


""""
Test if AddBookmarkCommand is successful
"""

def test_add_bookmark_command() -> None:
    a = AddBookmarkCommand()
    v_data = {
        "title": pytest.v_title ,
        "url": "htttp://tdd.com",
        "notes": "tdd",
        }
    a.execute(v_data)
    query = "SELECT 1 FROM  bookmarks WHERE title = ?"
    assert pytest.db._execute(query, (pytest.v_title,)).fetchone() is not None



""""
Test if ListBookmarksCommand is successful
"""

def test_list_bookmarks_command() -> None:
    a = ListBookmarksCommand()
    a.execute()
    v_results = pytest.db.select(pytest.table_name, order_by=1).fetchall()
    if v_results is None:
        assert "ERROR: Was not able to list bookmarks"


""""
Test if DeleteBookmarkCommand is successful
"""

def test_delete_bookmark_command() -> None:
    a = DeleteBookmarkCommand()
    query = "SELECT id FROM  " + pytest.table_name + " WHERE title = ?"
    v_id =  pytest.db._execute(query, (pytest.v_title,)).fetchone()[0]
    a.execute(v_id)
    query = "SELECT id FROM  " + pytest.table_name + " WHERE id = ?"
    v_id = pytest.db._execute(query, (v_id,)).fetchone()
    if v_id is not None:
        assert "ERROR: Was not able to delete bookmark"
