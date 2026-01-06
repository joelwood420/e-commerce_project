from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = '1995'


db = SQL("sqlite:///database/ecommerce.db")

products = db.execute("SELECT id, product_name as name, price, image_url FROM products")


@app.route('/')
def catalog():
    cart = get_cart()
    cart_item_count = sum(item['quantity'] for item in cart)
    return render_template('catalog.html', products=products, cart_item_count=cart_item_count)

def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    cart = get_cart()
    product_id = int(request.form['product_id'])

    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return redirect(url_for('catalog'))
    
    for item in cart: 
        if item["id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})

    session.modified = True
    return redirect(url_for('catalog'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    cart = get_cart()
    product_id = int(request.form['product_id'])

    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    cart = get_cart()
    total = sum(item['price'] * item['quantity'] for item in cart)
    cart_item_count = sum(item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total, cart_item_count=cart_item_count)

@app.route('/customer_details', methods=['GET', 'POST'])
def customer_details():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        db.execute("INSERT INTO customer_details (name, email, address) VALUES (?, ?, ?)", name, email, address)

        return redirect(url_for('order_confirmation'))

    return render_template('customer_details_form.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin_login_page():
    return render_template('admin_login.html')


@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = db.execute("SELECT username, password FROM admin_users WHERE username = ? AND password = ?", username, password)

    if user:
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin_login.html', error ='Invalid username or password')

@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return render_template('admin_login.html', error ='Please log in to access the dashboard')
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
