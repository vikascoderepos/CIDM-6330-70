from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services
from pprint import pprint
import json
from datetime import datetime, timezone
import uuid

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqllite_uri()))
app = Flask(__name__)

    
@app.route("/")
def index():
    return jsonify({'message': 'Barky App'}) 


@app.route("/bookmarks/", methods=["POST"])
def add_bookmark():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    content = request.get_json()
    date_added = datetime.now(timezone.utc)
    id=str(uuid.uuid4())

    bookmark = model.Bookmark(
            id, request.json["title"], request.json["url"], request.json["notes"], date_added
    )

    bookmarkref = services.add(bookmark, repo, session)
    return jsonify({'message': 'Barky App'}) 


@app.route("/bookmarks/<id>", methods=["POST"])
def edit_bookmark(id):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    content = request.get_json()
    date_added = datetime.now(timezone.utc)
    services.edit(id, request.json["title"], request.json["url"], request.json["notes"], date_added, repo, session)
    return jsonify({'message': 'Barky App'}) 



@app.route('/bookmarks/<id>/', methods=["DELETE"])
def delete_bookmark(id):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    message = services.delete(id, repo, session)
    return message;


@app.route('/bookmarks/<id>/', methods=["GET"])
def get_bookmark(id):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    bookmark = repo.get(id)
    return {
        'id': bookmark.id,
        'title': bookmark.title,
        'url': bookmark.url,
        'notes': bookmark.notes,
		'date_added': bookmark.date_added
    }

@app.route("/bookmarks", methods=["GET"])
def list_bookmark():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    bookmarks = repo.list()
    bookmarkList=[]
    for bookmark in bookmarks:
        bookmarkObject =  {
        'id': bookmark.id,
        'title': bookmark.title,
        'url': bookmark.url,
        'notes': bookmark.notes,
		'date_added': bookmark.date_added
    }
        bookmarkList.append(bookmarkObject)
    return jsonify(bookmarkList)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

