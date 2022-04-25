from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    note_data = db.Column(db.String(10000))
    post_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
    trade_id = db.Column(db.Integer, db.ForeignKey('trades.trade_id'))
    #add another foriegn key

class Trades(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True)
    item_desc = db.Column(db.String(512))
    item_type = db.Column(db.String)
    item_name = db.Column(db.String)
    active_trade = db.column(db.Boolean())
    item_condition = db.Column(db.String) 
    completed_trade = db.column(db.Boolean())   
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Notes')
    user_name = db.Column(db.String, db.ForeignKey('users.user_name'))

class Wishlist(db.Model):
    wishitem_id = db.Column(db.Integer, primary_key=True)
    user_name= db.Column(db.String, db.ForeignKey('users.user_name'))
    item_name = db.Column(db.String(15)) 


class Users(db.Model, UserMixin):
    email = db.Column(db.String(150), unique=True)
    user_password = db.Column(db.String(1000))
    user_name = db.Column(db.String, primary_key = True)
    shipping_address = db.column(db.String)
    notes = db.relationship('Notes') #relates the notes to each user
    trades= db.relationship('Trades') 
    iso = db.relationship('Wishlist')
    reputation = db.Column(db.Float(100.00))
    user = db.relationship('Users')
    id = db.Column(db.String, db.ForeignKey('users.user_name'))