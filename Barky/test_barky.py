from barky import *
from database import *
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
Test Option A) Add a bookmark
"""

def test_add_a_bookmark() -> None:
    a = commands.AddBookmarkCommand()
    v_data = {
        "title": pytest.v_title ,
        "url": "htttp://tdd.com",
        "notes": "tdd",
        }
    a.execute(v_data)
    query = "SELECT 1 FROM  bookmarks WHERE title = ?"
    assert pytest.db._execute(query, (pytest.v_title,)).fetchone() is not None


""""
Test Option (B) List bookmarks by date
"""

def test_list_bookmarks_by_date() -> None:
    a = commands.ListBookmarksCommand()
    results = a.execute()
    assert results is not None


""""
Test Option (T) List bookmarks by title
"""

def test_list_bookmarks_by_title() -> None:
    a = commands.ListBookmarksCommand(order_by="title")
    results = a.execute()
    assert results is not None

""""
Test Option (D) Delete a bookmark
"""

def test_delete_bookmark() -> None:
    a = commands.DeleteBookmarkCommand()
    query = "SELECT id FROM  " + pytest.table_name + " WHERE title = ?"
    v_id =  pytest.db._execute(query, (pytest.v_title,)).fetchone()[0]
    a.execute(v_id)
    query = "SELECT id FROM  " + pytest.table_name + " WHERE id = ?"
    v_id = pytest.db._execute(query, (v_id,)).fetchone()
    if v_id is not None:
        assert "ERROR: Was not able to delete bookmark"