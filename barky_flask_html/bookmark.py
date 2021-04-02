import os
import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime



app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookmarks.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Bookmark(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(1000))
        url = db.Column(db.String(1000))
        notes = db.Column(db.String(4000))
        date_added = db.Column(DateTime, default=datetime.datetime.utcnow)


        def __init__(self, title, url, notes):
            self.title = title
            self.url = url
            self.notes = notes



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

@app.route("/update", methods=["POST"])
def update():
    oldid = request.form.get("oldid")
    newtitle = request.form.get("newtitle")
    newurl = request.form.get("newurl")
    newnotes = request.form.get("newnotes")

    bookmark = Bookmark.query.filter_by(id=oldid).first()
    bookmark.title = newtitle
    bookmark.url = newurl
    bookmark.notes = newnotes

    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    oldid = request.form.get("oldid")
    bookmark = Bookmark.query.filter_by(id=oldid).first()
    db.session.delete(bookmark)
    db.session.commit()
    return redirect("/")


  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)