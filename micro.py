import os
import json

import requests
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

OFFERS_MS = os.environ["OFFERS_MS"]


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.Unicode(255))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    items_in_stock = db.Column(db.Integer)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship(
        "Product", backref=db.backref("offers", cascade="all,delete", lazy=True)
    )

    def serialize(self):
        return {
            "id": self.id,
            "price": self.price,
            "items_in_stock": self.items_in_stock,
        }


def request_token():
    try:
        f = open("token", "r")
        token = f.read()
    except FileNotFoundError:
        r = requests.post(OFFERS_MS + "/auth")
        token = json.loads(r.text)["access_token"]
        f = open("token", "w")
        f.write(token)
    return token


token = request_token()


def get_offers_all():
    for product_id in list(map(lambda x: x[0], db.session.query(Product.id).all())):
        get_offers(product_id)


def get_offers(product_id):
    r = requests.get(
        OFFERS_MS + "/products/" + str(product_id) + "/offers",
        headers={"Bearer": token},
    )
    for offer in r.json():
        offer_id = offer.get("id")
        offer_price = offer.get("price")
        offer_items_in_stock = offer.get("items_in_stock")
        db_offer = db.session.query(Offer).get(offer_id)
        if db_offer:
            if offer_price != db_offer.price:
                db_offer.price = offer_price
            if offer_items_in_stock != db_offer.items_in_stock:
                db_offer.items_in_stock = offer_items_in_stock
        else:
            db.session.add(
                Offer(
                    id=offer_id,
                    price=offer_price,
                    items_in_stock=offer_items_in_stock,
                    product_id=product_id,
                )
            )
    db.session.commit()


@app.route("/api/v1/products", methods=["GET"])
def get_products():
    return jsonify([prod.serialize() for prod in Product.query.all()])


@app.route("/api/v1/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    prod = Product.query.get(product_id)
    if prod is None:
        abort(404)
    return jsonify(prod.serialize())


@app.route("/api/v1/products", methods=["POST"])
def create_product():
    if not request.json or not "name" in request.json:
        abort(400)
    prod = Product(
        name=request.json["name"], description=request.json.get("description", "")
    )
    db.session.add(prod)
    db.session.commit()
    r = requests.post(
        OFFERS_MS + "/products/register",
        headers={"Bearer": token},
        data={"id": prod.id, "name": prod.name, "description": prod.description},
    )
    return jsonify({"id": prod.id}), 201


@app.route("/api/v1/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    prod = Product.query.get(product_id)
    if prod is None or not request.json:
        abort(404)
    prod.name = request.json.get("name", prod.name)
    prod.description = request.json.get("description", prod.description)
    db.session.commit()
    return jsonify(prod.serialize())


@app.route("/api/v1/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    prod = Product.query.get(product_id)
    if prod is None:
        abort(404)
    db.session.delete(prod)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0")
