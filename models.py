"""Models"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app as app, flash
from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), primary_key=False, nullable=False, unique=True)
    date_joined = db.Column(db.DateTime, index=False, nullable=True, unique=False)
    last_login = db.Column(db.DateTime, index=False, nullable=True, unique=False)
    cart = db.relationship('Cart', backref='buyer', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_to_cart(self, bottles_id, quantity):
        item_to_add = Cart(bottles_id=bottles_id, user_id=self.id, buy_quantity=quantity)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Wine added to cart! Success!')


class Cart(UserMixin, db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), nullable=True)
    buy_quantity = db.Column(db.Integer, nullable=True, default=1)

    def __repr__(self):
        return f"Cart('{self.id}', '{self.bottles_id}, '{self.user_id}', '{self.item_price}', '{self.buy_quantity}'))"


class Order(UserMixin, db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    order_total = db.Column(db.DECIMAL, nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}','{self.order_date}','{self.order_total}')"


class OrderedItems(UserMixin, db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.bottles_id}','{self.quantity}', '{self.item_price}')"


class Transactions(UserMixin, db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'), nullable=False)
    transaction_date = db.Column(db.DateTime,nullable=False)
    transaction_total = db.Column(db.DECIMAL, nullable=False)
    card_number = db.Column(db.String(50), nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.transaction_date}','{self.transaction_total}'," \
               f"'{self.card_number}'), '{self.card_type}', '{self.response}')"


class Bottles(UserMixin, db.Model):
    __tablename__ = 'bottles'
    __searchable__ = ['product_name', 'year', 'producer_name', 'country_name', 'region_name', 'color_name',
                      'primary_grape']
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(120), nullable=False)
    volume = db.Column(db.String(120), nullable=False)
    proof = db.Column(db.String(120), nullable=False)
    producer_name = db.Column(db.String(120), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country_name = db.Column(db.String(120), nullable=False)
    region_name = db.Column(db.String(120), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    appellation = db.Column(db.String(120), nullable=False)
    color_name = db.Column(db.String(120), nullable=False)
    primary_grape = db.Column(db.String(120), nullable=False)
    all_grape = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    countries = db.relationship('Countries', back_populates='bottles')
    stocks = db.relationship('Stocks', back_populates="bottles", uselist=False)

    def __repr__(self):
        return '<Bottles {}>'.format(self.product_name)


class Stocks(UserMixin, db.Model):
    __tablename__ = 'stocks'
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    bottles = db.relationship('Bottles', back_populates="stocks")

    def __repr__(self):
        return '<Stocks {}>'.format(self.quantity)


class Countries(UserMixin, db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(120), unique=True, nullable=False)

    bottles = db.relationship('Bottles', back_populates='countries')


class Regions(UserMixin, db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(120), unique=True, nullable=False)

