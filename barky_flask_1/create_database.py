from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import datetime
import os
import uuid

Base = declarative_base()

class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(String, primary_key=True)

    title = Column(String)
    url = Column(String, unique=True)
    notes = Column(String)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)


#engine = create_engine('sqllite:///:memory:' , echo=True)
#engine=create_engine('sqlite://',echo=True)
engine=create_engine('sqlite:///bookmarks.db',echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


session = Session()

bookmark = Bookmark()
bookmark.id = str(uuid.uuid4())
bookmark.title = "test2"
bookmark.url = "http://test2.com"
bookmark.notes = "test2 notes"
session.add(bookmark)
session.commit()

bookmark = Bookmark()
bookmark.id = str(uuid.uuid4())
bookmark.title = "test1"
bookmark.url = "http://test1.com"
bookmark.notes = "test1 notes"
session.add(bookmark)
session.commit()

session.close()