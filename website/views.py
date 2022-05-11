from asyncio.windows_events import NULL
from hashlib import new
from re import T
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user,logout_user
from sqlalchemy import false, true, text
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from website.dbfunc import get_active_trades, get_num_trades
from src.models import Notes
from src.models import Users
from src.models import Trades
from src.models import db
import os
import json
from better_profanity import profanity

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/search')
def search():
    return render_template("search.html", user=current_user)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/delete')
def delete():
    return render_template("delete.html", user=current_user)

@views.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    all_trades = Trades.query.all()
    db.session.commit()
    return render_template("trade.html", user=current_user, all_trades = all_trades)

@views.route('/trade/<int:trade_id>', methods=['POST','GET'])
def get_trade(trade_id):
    trade = Trades.query.get(trade_id)
    all_notes = Notes.query.filter_by(trade_id=trade_id).all()
    db.session.commit()
    if not trade:
        # TODO: Code for if the trade ID cannot be found. Currently just sends user back to homepage
        flash("ERROR: Could not find trade with ID " + str(trade_id) + ", redirected back home.")
        return render_template("home.html", user=current_user)
    if request.method == 'POST':
        note_data = request.form.get('msg')
        censored_data = profanity.censor(note_data) #checks to see if their is profanity in this sentence
        if len(censored_data) == 0:
            flash('In order to post a note you must ')
        elif len(censored_data) < 10:
            flash('Note is too short, must be 10 characters')
        else:
            new_note = Notes(note_data = censored_data, user_name = current_user.user_name,
            trade_id = trade_id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.get_trade', trade_id=trade_id))

    return render_template("singletrade.html", user=current_user, trade = trade, trade_notes = all_notes)

@views.route('/createtrade', methods=['GET', 'POST'])
@login_required
def createtrade():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_type = request.form.get('item_type')
        item_desc = request.form.get('desc')
        item_condition = request.form.get('condition')
        file = request.files['file']

        conds = ['New','Used','Refurbished','For Parts']
        types = ['Video Games','Collectibles','Small Electronics','Computers','Other']

        if len(item_name) < 2:
            flash('Item name is too short!')
        elif item_type not in types:
            flash('Please select a item type or other')
        elif item_desc == NULL:
            flash('Item description is required')
        elif len(item_desc) < 10:
            flash("Item description is not comprehensive enough")
        elif item_condition not in conds:
            flash('Please select a item condition')
        else:
            new_trade = Trades(item_name = item_name, item_type = item_type, 
            item_desc = item_desc, item_condition = item_condition, active_trade = True, 
            completed_trade = False, user_name = current_user.user_name)
            db.session.add(new_trade)
            db.session.commit()
            if file:
                print("got here woooo")
                file = request.files['file']
                if not os.path.exists('/website/static/images'):
                    os.makedirs('/website/static/images')
                filename = str(new_trade.trade_id) + ".png"
                file.save(os.path.join("/website/static/images/", filename))
            return redirect(url_for('views.get_trade',trade_id=new_trade.trade_id))
    return render_template("create.html", user=current_user)


@views.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
    user_name = current_user.user_name
    user_trades = Trades.query.get(user_name)
    db.session.commit()
    return render_template("userpage.html", user=current_user, user_trades = user_trades)

@views.route('/usersettings',methods=['GET', 'POST'])
@login_required
def usersettings():
    if request.method == 'POST':

        user_to_update = Users.query.get_or_404(current_user.user_name)
        old_password = current_user.user_password
        old_email = current_user.email

        display_name = request.form.get('username') #idk if it is safe to update it
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        conf_password = request.form.get('confirm_password')
        shipping_address = request.form.get('address')
        
        if new_password != old_password:
            if len(new_password) < 7:
                if new_password == conf_password:
                    user_password=generate_password_hash(new_password, method='sha256')
                    user_to_update.user_password = user_password
                else:
                    flash('Passwords must match')

        if new_email == 'None':
            user_to_update.email = old_email
        else:
            
            user_to_update.email = new_email

        user_to_update.shipping_address = shipping_address

        db.session.commit()
        return redirect(url_for('views.userpage',user =current_user))    

    return render_template("usersettings.html", user=current_user)

@views.route('/updatenote',methods=['GET', 'POST'])
@login_required
def delete_user():
    user_to_delete = Users.query.get_or_404(current_user.user_name)
    db.session.delete(user_to_delete)
    db.session.commit()
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/updatenote',methods=['GET', 'POST'])
@login_required
def update_note(note_id,trade_id):
    note_to_update = Notes.query.get_or_404(note_id)
    if request.method == 'POST':
        new_data = request.form.get('note_data')
        if len(new_data) < 10:
            flash('Note must contain at least 10 characters')
        else:
            censored_data = profanity.censor(censored_data)
            note_to_update.note_data = new_data
            db.session.commit()
            return redirect(url_for('views.get_trade', trade_id=trade_id))

@views.route('/deletenote',methods=['GET', 'POST'])
@login_required
def delete_note(note_id, trade_id):
    note_to_delete = Notes.query.get_or_404(note_id)
    if note_to_delete.user_name == current_user.user_name:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect(url_for('views.get_trade', trade_id=trade_id))


def processimg():
    return