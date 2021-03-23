from database import *
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
v_table_name = 'bookmarks' + date_time
pytest.db_file = "bookmarks1.db"
pytest.table_name = v_table_name
pytest.date_time = date_time
pytest.v_title = "##########Test Data#################" + pytest.date_time
pytest.v_date =  now.strftime('%Y-%m-%d %H:%M:%S')
pytest.db = DatabaseManager(pytest.db_file)


""""
Testing if there are privileges to create a table and to establish a session to database
"""

def test_create_table() -> None:
  pytest.db.create_table(
        pytest.table_name,
         {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
          },
    )
  query = "SELECT 1 FROM sqlite_master WHERE type='table' and name = ?"
  assert pytest.db._execute(query, (pytest.table_name,)).fetchone() is not None

""""
Testing if we are able to add a record to the table
"""
def test_add() -> None:
  pytest.db.add(
        pytest.table_name,
         {
            "title": pytest.v_title ,
            "url": "htttp://tdd.com",
            "notes": "tdd",
            "date_added": pytest.v_date ,
          },
    )
  query = "SELECT 1 FROM  " + pytest.table_name + " WHERE title = ?"
  assert pytest.db._execute(query, (pytest.v_title,)).fetchone() is not None




""""
Testing if we are able to select from the table
"""
def test_select() -> None:
  v_results = pytest.db.select(pytest.table_name, order_by=1).fetchall()
  if v_results is None:
    assert "ERROR: Was not able to select from the database"


""""
Testing if we are able to delete a record to the table
"""
def test_delete() -> None:
  query = "SELECT id FROM  " + pytest.table_name + " WHERE title = ?"
  v_id =  pytest.db._execute(query, (pytest.v_title,)).fetchone()[0]
  pytest.db.delete(pytest.table_name, {"id": v_id})
  query = "SELECT 1 FROM  " + pytest.table_name + " WHERE title = ?"
  assert pytest.db._execute(query, (pytest.v_title,)).fetchone() is  None


