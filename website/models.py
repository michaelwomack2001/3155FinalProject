from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500))
    item_type = db.Column(db.String(500))
    item_name = db.Column(db.String(500))
    size = db.Column(db.Integer())
    active_trade = db.column(db.Boolean())
    condition = db.Column(db.String(500)) 
    completed = db.column(db.Boolean())   
    tag = db.column(db.Boolean())   
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ISO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    item_name = db.Column(db.String(15)) 


class DISO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_1 = db.Column(db.String(15)) 


class Listings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500))
    item_type = db.Column(db.String(500))
    item_name = db.Column(db.String(500))
    price = db.column(db.Float())
    active_listing = db.column(db.Boolean())
    completed = db.column(db.Boolean())
    tag = db.column(db.Boolean())
    condition = db.Column(db.String(500))  
    size = db.Column(db.Integer())     
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_name = db.Column(db.String, db.ForeignKey('user.user_name'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    is_premium = db.Column(db.Boolean())
    notes = db.relationship('Note') #relates the notes to each user
    trades= db.relationship('Trades') 
    notes = db.relationship('Listings') 
    diso = db.relationship('DISO')
    iso = db.relationship('ISO')
    reputation = db.Column(db.Float(100.00))
    Shipping_Address = db.relationship('Shipping_Address') #relates the user to the shipping address
    Billing_Address = db.relationship('Billing_Address') #relates the user to the shipping address


class Shipping_Address(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    street_address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    room_number = db.Column(db.Integer())
    building_number = db.Column(db.Integer())
    zip_code = db.Column(db.Integer())
    reputation = db.Column(db.Float(100.00))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Billing_Address(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    street_address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    room_number = db.Column(db.Integer())
    building_number = db.Column(db.Integer())
    zip_code = db.Column(db.Integer())
    reputation = db.Column(db.Float(100.00))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#add a site admin with dashboard setting i.e. remove user, ban user, change reputation, etc... 