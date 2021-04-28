from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from addition.domain import model
from addition.adapters import orm
from addition.service_layer import services, unit_of_work



app = Flask(__name__)
orm.start_mappers()


@app.route("/add_product", methods=['POST'])
def add_product():

    maxAllowedPurchaseQty = request.json['maxAllowedPurchaseQty']
    if maxAllowedPurchaseQty is not None:
        services.add_product(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        maxAllowedPurchaseQty,
        request.json["brand"],
        request.json["price"],
        unit_of_work.SqlAlchemyUnitOfWork(),
    )
    return "OK", 201

@app.route("/add", methods=['POST'])
def add_endpoint():
    try:
        productref = services.add(
            request.json['itemid'],
            request.json['sku'],
            request.json['qty'],
            unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"productref": productref}, 201





if __name__ == "__main__":
    app.run(host='localhost', debug=True)
