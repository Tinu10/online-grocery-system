from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blinkit_secret"

# USERS
users = {"user": "123"}

# PRODUCTS
products = {
    "Milk": [{"name": "Milk", "price": 80}],
    "Rice": [{"name": "Rice", "price": 100}],
    "Vegetables": [
        {"name": "Carrot", "price": 50},
        {"name": "Potato", "price": 30},
        {"name": "Tomato", "price": 40},
        {"name": "Onion", "price": 35},
        {"name": "Cabbage", "price": 25},
        {"name": "Cauliflower", "price": 45},
        {"name": "Spinach", "price": 30},
        {"name": "Peas", "price": 80},
        {"name": "Capsicum", "price": 70},
        {"name": "Broccoli", "price": 120}
    ],
    "Fruits": [
        {"name": "Apple", "price": 120},
        {"name": "Banana", "price": 60},
        {"name": "Mango", "price": 100},
        {"name": "Orange", "price": 80},
        {"name": "Grapes", "price": 150},
        {"name": "Pineapple", "price": 90},
        {"name": "Strawberry", "price": 200},
        {"name": "Watermelon", "price": 50},
        {"name": "Papaya", "price": 60},
        {"name": "Kiwi", "price": 300}
    ]
}

orders = {}

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if users.get(u) == p:
            session.clear()
            session["user"] = u
            session["cart"] = {}
            orders[u] = []  # clear old orders
            return redirect("/products")
    return render_template("login.html")

# PRODUCTS PAGE
@app.route("/products")
def products_page():
    if "user" not in session:
        return redirect("/")
    return render_template("products.html", products=products)

# ADD TO CART
@app.route("/add", methods=["POST"])
def add_to_cart():
    item = request.form["item"]
    price = int(request.form["price"])
    cart = session.get("cart", {})
    if item in cart:
        cart[item]["qty"] += 1
    else:
        cart[item] = {"price": price, "qty": 1}
    session["cart"] = cart
    return redirect("/products")

# CART PAGE
@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect("/")
    cart = session.get("cart", {})
    total = sum(v["price"] * v["qty"] for v in cart.values())
    return render_template("cart.html", cart=cart, total=total)

# PAYMENT PAGE
@app.route("/payment", methods=["GET", "POST"])
def payment():
    cart = session.get("cart", {})
    total = sum(v["price"] * v["qty"] for v in cart.values())
    gst = round(total * 0.05, 2)
    delivery = 30
    final = total + gst + delivery

    if request.method == "POST":
        payment_type = request.form.get("payment_type", "online")
        orders[session["user"]].append({
            "order_items": cart,
            "amount": final,
            "payment_type": payment_type,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        })
        session["cart"] = {}
        return redirect("/orders")

    return render_template("payment.html", total=total, gst=gst, delivery=delivery, final=final)

# ORDERS PAGE
@app.route("/orders")
def orders_page():
    if "user" not in session:
        return redirect("/")
    return render_template("orders.html", orders=orders.get(session["user"], []))

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

'''if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)'''


if __name__ == "__main__":
    app.run()
