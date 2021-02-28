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
pytest.table_name = "v_table_name"
print(v_table_name)    
  
""""
Testing if there are privileges to create a table and to establish a session to database
"""

def test_create_table() -> None:
  print(v_table_name)    
  db = DatabaseManager(pytest.db_file)
  db.create_table(
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
  assert db._execute(query, (pytest.table_name,)).fetchone() is not None




""""
Testing if we are able to add a record to the table
"""
def test_add_record() -> None:
  print(v_table_name)    
  db = DatabaseManager(pytest.db_file)
  v_title = "##########Test Data#################" + date_time
  v_date =  "now.strftime('%Y-%m-%d %H:%M:%S')"
  db.add(
        pytest.table_name,
         {
            "title": v_title ,
            "url": "htttp://tdd.com",
            "notes": "tdd",
            "date_added": v_date ,
          },
    )
  #query = "SELECT 1 FROM "+ pytest.table_name + " WHERE title = ?"
  #assert db._execute(query, (pytest.table_name,) ).fetchone() is not None

