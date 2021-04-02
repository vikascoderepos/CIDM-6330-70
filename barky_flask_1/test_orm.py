import model
from datetime import date

def test_bookmark_mapper_can_load_bookmarks(session):
    session.execute(
        "INSERT INTO bookmarks (id, title, url, notes, date_added) VALUES "
'(1,"google","https://www.google.com/","google website", "2021-03-24 03:56:33.961691"),'
'(2,"google1","https://www.google1.com/","google1 website", "2021-03-24 03:56:33.961691"),'
'(3,"google2","https://www.google2.com/","google2 website", "2021-03-24 03:56:33.961691"),'
    )
    expected = [
        model.OrderLine(1,"google","https://www.google.com/","google website", "2021-03-24 03:56:33.961691"),
        model.OrderLine(2,"google1","https://www.google1.com/","google1 website", "2021-03-24 03:56:33.961691"),
        model.OrderLine(3,"google2","https://www.google2.com/","google2 website", "2021-03-24 03:56:33.961691"),
    ]
    assert session.query(model.Bookmark).all() == expected


def test_bookmark_mapper_can_save_bookmarks(session):
    new_bookmark = model.Bookmark(4,"google4","https://www.google4.com/","google4 website", "2021-03-24 03:56:33.961691")
    session.add(new_bookmark)
    session.commit()

    rows = list(session.execute('SELECT id, title, url, notes, date_added  FROM "bookmarks"'))
    assert rows == [(4,"google4","https://www.google4.com/","google4 website", "2021-03-24 03:56:33.961691")]



