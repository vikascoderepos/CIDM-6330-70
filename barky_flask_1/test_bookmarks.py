from datetime import date
from model import Bookmark

def test_cannot_add_same_url_multiple_times():
    bookmark1 = Bookmark("dc3a2e08-9e2b-4838-9719-bd1ce4a647b1", "google", 'https://www.google.com/', 'first notes', date.today())
    bookmark2 = Bookmark("dc3a2e08-9e2b-4838-9719-bd1ce4a647b2", "google", 'https://www.google.com/', 'seconnd notes', date.today())

