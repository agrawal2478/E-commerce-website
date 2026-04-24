from flask import Flask, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # New table with image
    c.execute('''
        CREATE TABLE IF NOT EXISTS products
        (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, image TEXT)
    ''')

    # Clear old data (optional)
    c.execute("DELETE FROM products")

    products = [
        ("Laptop Dell", 50000, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
        ("iPhone 13", 70000, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"),
        ("Headphones Sony", 3000, "https://images.unsplash.com/photo-1518444028785-8fcb2c9b5fdf"),
        ("Smart Watch", 4000, "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b"),
        ("Bluetooth Speaker", 2500, "https://images.unsplash.com/photo-1585386959984-a415522316a3"),
        ("Gaming Mouse", 1500, "https://images.unsplash.com/photo-1587202372775-e229f172b9d4"),
        ("Mechanical Keyboard", 3500, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
        ("Monitor 24 inch", 12000, "https://images.unsplash.com/photo-1587202372775-e229f172b9d4"),
        ("Tablet Samsung", 20000, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"),
        ("Power Bank", 1200, "https://images.unsplash.com/photo-1585386959984-a415522316a3"),
        ("Wireless Earbuds", 2500, "https://images.unsplash.com/photo-1518444028785-8fcb2c9b5fdf"),
        ("DSLR Camera", 45000, "https://images.unsplash.com/photo-1519183071298-a2962be96f6e"),
        ("Tripod Stand", 1500, "https://images.unsplash.com/photo-1519183071298-a2962be96f6e"),
        ("External HDD", 5000, "https://images.unsplash.com/photo-1587202372775-e229f172b9d4"),
        ("SSD 1TB", 8000, "https://images.unsplash.com/photo-1587202372775-e229f172b9d4"),
        ("Graphics Card", 30000, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
        ("Router WiFi", 2000, "https://images.unsplash.com/photo-1585386959984-a415522316a3"),
        ("Smart TV", 35000, "https://images.unsplash.com/photo-1593784991095-a205069470b6"),
        ("Projector", 18000, "https://images.unsplash.com/photo-1593784991095-a205069470b6"),
        ("VR Headset", 25000, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
        ("Drone Camera", 60000, "https://images.unsplash.com/photo-1508614589041-895b88991e3e"),
        ("Microphone", 4000, "https://images.unsplash.com/photo-1518444028785-8fcb2c9b5fdf"),
        ("USB Hub", 800, "https://images.unsplash.com/photo-1585386959984-a415522316a3"),
        ("Cooling Pad", 1200, "https://images.unsplash.com/photo-1587202372775-e229f172b9d4"),
        ("Smart Bulb", 700, "https://images.unsplash.com/photo-1585386959984-a415522316a3"),
        ("Webcam HD", 2500, "https://images.unsplash.com/photo-1519183071298-a2962be96f6e"),
        ("Printer", 9000, "https://images.unsplash.com/photo-1593784991095-a205069470b6"),
        ("Scanner", 6000, "https://images.unsplash.com/photo-1593784991095-a205069470b6"),
        ("Game Controller", 3500, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
        ("Smart Glasses", 15000, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8")
    ]

    for i, p in enumerate(products, start=1):
        c.execute("INSERT INTO products VALUES (?, ?, ?, ?)", (i, p[0], p[1], p[2]))

    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)


@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(id)
    session.modified = True
    return redirect('/')


@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    if 'cart' in session:
        session['cart'] = [x for x in session['cart'] if x != id]
        session.modified = True
    return redirect('/cart')


@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    items = []
    total = 0

    for id in cart_ids:
        c.execute("SELECT * FROM products WHERE id=?", (id,))
        p = c.fetchone()
        if p:
            items.append(p)
            total += p[2]

    conn.close()
    return render_template("cart.html", items=items, total=total)


@app.route('/checkout')
def checkout():
    session['cart'] = []
    return render_template("checkout.html")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
