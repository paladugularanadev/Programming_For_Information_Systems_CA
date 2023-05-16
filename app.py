from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, session, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranadev_app.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)

db.create_all()

@app.route("/")
def index():
    products = db.execute("SELECT * FROM products ORDER BY team ASC")
    productsLen = len(products)
    # Initialize variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        products = db.execute("SELECT * FROM products ORDER BY team ASC")
        productsLen = len(products)
        return render_template ("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen, productsLen=productsLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ( "index.html", products=products, shoppingCart=shoppingCart, productsLen=productsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5050)
