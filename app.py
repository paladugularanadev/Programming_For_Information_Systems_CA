from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session, jsonify

# # Instantiate Flask object named app
app = Flask(__name__)

# # Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL ( "sqlite:///ranadev_app.db" )

@app.route("/")
def index():
    products = db.execute("SELECT * FROM products ORDER BY product ASC")
    productsLen = len(products)
    
    # Initialize variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT product, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY product")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        products = db.execute("SELECT * FROM products ORDER BY product ASC")
        productsLen = len(products)
        return render_template("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen, productsLen=productsLen, total=total, totItems=totItems, display=display, session=session)
    return render_template("index.html", products=products, shoppingCart=shoppingCart, productsLen=productsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)

