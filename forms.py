from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length, InputRequired, Email, EqualTo, Optional
from flask_login import login_user, current_user, logout_user, login_required

from .models import *
#
#
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(4)])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')
#
#
# class RegistrationForm(FlaskForm):
#     username = StringField('Username', [DataRequired()])
#     email = StringField('Email', validators=[
#                 Length(min=4), Email(message='Enter a valid email.'), DataRequired()])
#     password = PasswordField('Password', validators=[
#                 DataRequired(), Length(min=4, message='Please select a stronger password.')])
#     password2 = PasswordField('Confirm Your Password', validators=[
#                 DataRequired(), EqualTo('password', message='Passwords must match.')])
#     submit = SubmitField('Register')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')
#

# FlaskForm for checkout details
class checkoutForm(FlaskForm):
    fullname = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    card_type = RadioField('card_type')
    card_number = StringField('Credit card number',
                           validators=[DataRequired()])
    expdate = StringField('Exp Date',
                           validators=[DataRequired(), Length(min=12, max=12)])
    cvv = StringField('CVV',
                      validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('MAKE PAYMENT')


# Adds data to OrderedItems table
def updateStock(user_id):
        cart = Cart.query.join(Stocks, Cart.bottles_id == Stocks.bottles_id). \
            add_columns(Stocks.quantity, Cart.buy_quantity, Stocks.bottles_id, Cart.bottles_id). \
            filter(Cart.user_id == user_id).all()


# Adds data to OrderedItems table
def updateOrderedItems(order_id, user_id):
    cart = Cart.query.with_entities(Cart.bottles_id, Cart.buy_quantity).filter(Cart.user_id == user_id)
    for item in cart:
        ordered_cart_item = OrderedItems(order_id=order_id, bottles_id=item.bottles_id, quantity=item.buy_quantity)
        db.session.add(ordered_cart_item)
        db.session.commit()


# Removes sold products from user's cart
def removeOrderedfromCart(user_id):
    db.session.query(Cart).filter(Cart.user_id == user_id).delete()
    db.session.commit()


# Updates the Transactions table for record of transactions
def updateTransactions(order_id, order_date, order_total, card_number, card_type):
    transaction = Transactions(order_id=order_id, transaction_date=order_date, transaction_total=order_total,
                                       card_number=card_number, card_type=card_type, response='success')
    db.session.add(transaction)
    db.session.flush()
    db.session.commit()
