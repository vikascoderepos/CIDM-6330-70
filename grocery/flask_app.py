from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import scoped_session 

import config
import model
import orm
import repository
import services


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
# get_session = scoped_session(sessionmaker(bind=create_engine(config.get_postgres_uri())))
app = Flask(__name__)


@app.route("/add", methods=["POST"])
def add_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    item = model.CartItem(
        request.json["itemid"], request.json["sku"], request.json["qty"],
    )

    try:
        productref = services.add(item, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"productref": productref}, 201




if __name__ == "__main__":
    app.run(host='localhost', debug=True)
