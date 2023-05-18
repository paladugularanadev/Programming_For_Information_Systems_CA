from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL ( "sqlite:///ranadev_app.db" )

@app.route("/")
def index():
    products = db.execute("SELECT * FROM products ORDER BY product ASC")
    productsLen = len(products)
    

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

@app.route("/logout/")
def logout():
    
    db.execute("DELETE from cart")
    
    session.clear()
    
    return redirect("/")


@app.route("/register/", methods=["POST"] )
def registration():
    
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    
    rows = db.execute( "SELECT * FROM users WHERE username = :username ", username = username )
    
    if len( rows ) > 0:
        return render_template ( "register.html", msg="Username exists!" )
    
    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:username, :password, :fname, :lname, :email)",
                    username=username, password=password, fname=fname, lname=lname, email=email )
    
    return render_template ( "login.html" )


@app.route("/cart/")
def cart():
    if 'user' in session:
        
        totItems, total, display = 0, 0, 0
        
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY product")
        
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
    
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/register/", methods=["GET"])
def new():
    # Render log in page
    return render_template("register.html")


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/checkout/")
def checkout():
    order = db.execute("SELECT * from cart")
    
    for item in order:
        db.execute("INSERT INTO purchases (uid, id, image, quantity) VALUES(:uid, :id, :image, :quantity)", uid=session["uid"], id=item["id"], image=item["image"], quantity=item["qty"] )
   
    db.execute("DELETE from cart")
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    
    return redirect('/')

@app.route("/buy/")
def buy():
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
       
        id = int(request.args.get('id'))
       
        goods = db.execute("SELECT * FROM products WHERE id = :id", id=id)
        
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        product = goods[0]["product"]
        image = goods[0]["image"]
        subTotal = qty * price
        
        db.execute("INSERT INTO cart (id, qty, product, image, price, subTotal) VALUES (:id, :qty, :product, :image, :price, :subTotal)", id=id, qty=qty, product=product, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT product, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY product")
        shopLen = len(shoppingCart)
       
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
       
        products = db.execute("SELECT * FROM products ORDER BY product ASC")
        productsLen = len(products)
       
        return render_template("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen, productsLen=productsLen, total=total, totItems=totItems, display=display, session=session )

@app.route("/logged/", methods=["POST"] )
def logged():
    user = request.form["username"].lower()
    pwd = request.form["password"]
    
    if user == "" or pwd == "":
        return render_template("login.html")
    query = "SELECT * FROM users WHERE username = :user AND password = :pwd"
    rows = db.execute ( query, user=user, pwd=pwd )

    
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = rows[0]["id"]
    
    if 'user' in session:
        return redirect ( "/" )
    
    return render_template ( "login.html", msg="Wrong username or password." )

@app.route("/remove/", methods=["GET"])
def remove():
   
    out = int(request.args.get("id"))
   
    db.execute("DELETE from cart WHERE id=:id", id=out)
    
    totItems, total, display = 0, 0, 0
    
    shoppingCart = db.execute("SELECT product, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY product")
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    
    display = 1
    
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/history/")
def history():
   
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0

    myproducts = db.execute("SELECT * FROM purchases WHERE uid=:uid", uid=session["uid"])
    myproductsLen = len(myproducts)
   
    return render_template("history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myproducts=myproducts, myproductsLen=myproductsLen)

