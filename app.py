from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = '1995'


products = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99},
    {'id': 2, 'name': 'Smartphone', 'price': 499.99},
    {'id': 3, 'name': 'Tablet', 'price': 299.99},
    {'id': 4, 'name': 'Headphones', 'price': 199.99}
]


@app.route('/')
def catalog():
    return render_template('catalog.html', products=products)
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


@app.route('/cart')
def view_cart():
    cart = get_cart()
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)
