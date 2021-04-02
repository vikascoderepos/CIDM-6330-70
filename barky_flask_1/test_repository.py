import model
import repository


def insert_bookmark(session):
    session.execute(
        "INSERT INTO bookmarks (id, title, url, notes, date_added)"
        ' VALUES (5,"google5","https://www.google5.com/","google5 website", "2021-03-24 03:56:33.961691")'
    )
    [[bookmark_url]] = session.execute(
        "SELECT url FROM bookmarks WHERE url=:url ",
        dict(url="https://www.google5.com/"),
    )
    return bookmark_url


def test_repository_can_save_a_bookmark(session):
    bookmark = model.Bookmark(6,"google6","https://www.google6.com/","google6 website", "2021-03-24 03:56:33.961691")

    repo = repository.SqlAlchemyRepository(session)
    repo.add(bookmark)
    session.commit()

    rows = session.execute(
        'SELECT id, title, url, notes, date_added FROM "bookmarks"'
    )
    assert list(rows) == [(6,"google6","https://www.google6.com/","google6 website", "2021-03-24 03:56:33.961691")]


