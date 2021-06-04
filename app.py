from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=False)
    description = db.Column(db.String(144), unique=False)
    photo = db.Column(db.String(2000), unique=False)
    price = db.Column(db.Float, unique=False)
    sale = db.Column(db.String(3), unique=False)
    availableProduct = db.Column(db.Integer, unique=False)

    def __init__(self, title, description, photo, price, sale, availableProduct):
        self.title = title
        self.description = description
        self.photo = photo
        self.price = price
        self.sale = sale
        self.availableProduct = availableProduct

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description', 'photo', 'price', 'sale', 'availableProduct')

@app.route('/')
def hello():
    return "this works"

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product', methods=['POST'])
def add_product():
    title = request.json['title']
    description = request.json['description']
    photo = request.json['photo']
    price = request.json['price']    
    sale = request.json['sale']
    availableProduct = request.json['availableProduct']

    new_product = Product(title, description, photo, price, sale, availableProduct)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)

# endpoint to query all products
@app.route('/products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Endpoint for querying a single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
	product = Product.query.get(id)
	return product_schema.jsonify(product)


# Endpoint for updating a product
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    title = request.json['title']
    description = request.json['description']
    photo = request.json['photo']
    price = request.json['price']
    sale = request.json['sale']
    availableProduct = request.json['availableProduct']

    product.title = title
    product.description = description
    product.photo = photo
    product.price = price
    product.sale = sale
    product.availableProduct = availableProduct

    db.session.commit()
    return product_schema.jsonify(product)

#Endpoint for deleting a product
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
	product = Product.query.get(id)
	db.session.delete(product)
	db.session.commit()

	return product_schema.jsonify(product)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    firstName = db.Column(db.String(40), unique=False)
    lastName = db.Column(db.String(40), unique=False)
    password = db.Column(db.String(60), unique=False)
    cardNumber = db.Column(db.Integer, unique=True)
    cardCRV = db.Column(db.Integer, unique=False)
    cardAddress = db.Column(db.String(60), unique=False)
    cardName = db.Column(db.String(80), unique=False)

    def __init__(self, email, firstName, lastName, password, cardNumber, cardCRV, cardAddress, cardName):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.cardNumber = cardNumber
        self.cardCRV = cardCRV
        self.cardAddress = cardAddress
        self.cardName = cardName

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'firstName', 'lastName', 'password', 'cardNumber', 'cardCRV', 'cardAddress', 'cardName')

user_schema = UserSchema()

# Endpoint for creating a new user
@app.route('/user', methods=['POST'])
def add_user():
    email = request.json['email']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    password = request.json['password']
    cardNumber = request.json['cardNumber']
    cardCRV = request.json['cardCRV']
    cardAddress = request.json['cardAddress']
    cardName = request.json['cardName']

    new_user = User(email, firstName, lastName, password, cardNumber, cardCRV, cardAddress, cardName)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)


# Endpoint for querying a single user
@app.route("/user/<id>", methods=["GET"])
def get_user(id):
	user = User.query.get(id)
	return user_schema.jsonify(user)

# Endpoint for updating a user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    email = request.json['email']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    password = request.json['password']
    cardNumber = request.json['cardNumber']
    cardCRV = request.json['cardCRV']
    cardAddress = request.json['cardAddress']
    cardName = request.json['cardName']
    
    user.email = email
    user.firstName = firstName
    user.lastName = lastName
    user.password = password
    user.cardNumber = cardNumber
    user.cardCRV = cardCRV
    user.cardAddress = cardAddress
    user.cardName = cardName

    db.session.commit()
    return user_schema.jsonify(user)

#Endpoint for deleting a user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()

	return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)