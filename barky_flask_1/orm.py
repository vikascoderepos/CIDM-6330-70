from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper

import model
import datetime

metadata = MetaData()

bookmarks = Table('bookmarks', metadata,
            Column('id', String, primary_key=True),
            Column('title', String(255), nullable=False),
            Column('url', String(255), nullable=False, unique=True),
            Column('notes', String(255)),
			Column('date_added', default=datetime.datetime.utcnow)
        )


def start_mappers():
    mapper(model.Bookmark, bookmarks)