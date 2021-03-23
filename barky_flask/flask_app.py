from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqllite_uri()))
app = Flask(__name__)




@app.route("/", methods=["GET", "POST"])
def home():
    bookmarks = None
    if request.form:
        try:
            bookmark = Bookmark(title=request.form.get("title") , url=request.form.get("url"), notes=request.form.get("notes"))
            db.session.add(bookmark)
            db.session.commit()
        except Exception as e:
            print("Failed to add bookmarks")
            print(e)
    #bookmarks = Bookmark.query.all()
    bookmarks_by_date = Bookmark.query.filter().order_by('date_added')
    bookmarks_by_title = Bookmark.query.filter().order_by('title')
    #return render_template("home.html", bookmark=bookmarks)
    return render_template("home.html", bookmarks_by_date=bookmarks_by_date, bookmarks_by_title=bookmarks_by_title)



    


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201