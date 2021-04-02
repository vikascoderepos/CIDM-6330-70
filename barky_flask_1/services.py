from __future__ import annotations

import model
from model import Bookmark
from repository import AbstractRepository




def add(bookmark: Bookmark, repo: AbstractRepository, session) -> str:
    session.add(bookmark)
    session.commit()
    return {
		'success': 'Data added successfully'
	}


def delete(id: id, repo: AbstractRepository, session) -> str:
    bookmark = repo.get(id)
    session.delete(bookmark)
    session.commit()
    return {
		'success': 'Data deleted successfully'
	}

def edit(id: id, title: title, url: url, notes: notes , date_added: date_added , repo: AbstractRepository, session) -> str:
    bookmark = repo.get(id)
    bookmark.title = title
    bookmark.url = url
    bookmark.notes = notes
    bookmark.date_added = date_added
    session.commit()
    return {
		'success': 'Data deleted successfully'
	}