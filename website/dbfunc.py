from pickle import TRUE
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from sqlalchemy import false, true
from werkzeug.security import generate_password_hash, check_password_hash

from website.models import Listings, Trades
from . import db
import json

#Trader Functions

def get_num_trades(current_user):
    num_trades = 0
    for i in current_user.trades:
        num_trades += 1
    return num_trades

def get_active_trades(current_user):
    active_trades = 0
    return active_trades

def get_completed_trades(current_user):
    completed_trades = 0

    return completed_trades

#Seller Functions
""""""""""
def get_num_listings(current_user):
    num_listings = 0
    for i in current_user.listings:
        num_listings += 1
    return num_listings

def get_active_listings(current_user):
    num_listings = 0
    for i in current_user.listings:
        if i.active_listing == True:
            num_listings += 1
    return num_listings

def get_completed_listings(current_user):
    completed_listings = 0
    for i in Listings:
        if i.user_id == current_user.user_id:
            if i.completed == True:
                completed_listings += 1
    return completed_listings
"""""""""