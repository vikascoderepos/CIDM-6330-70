from __future__ import annotations
from datetime import date
from typing import Optional, List, Set


class Bookmark:
    def __init__(self, id: str, title: str, url: str, notes: str, date_added: datetime):
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added

    def __repr__(self):
        return f"<Bookmark {self.url}>"

    def __eq__(self, other):
        if not isinstance(other, Bookmark):
            return False
        return other.url == self.url

