from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from sqlalchemy import false, true
from werkzeug.security import generate_password_hash, check_password_hash

from website.dbfunc import get_active_trades, get_num_trades
from .models import Note
from .models import User
from .models import Trades
from . import db
import json

views = Blueprint('views', __name__)

# https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/



@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/search')
def search():
    return render_template("search.html", user=current_user)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            
    return render_template("trade.html", user=current_user, trades= Trades.query.all())

@views.route('/buysell')
@login_required
def buysell():
    return render_template("BuySell.html", user=current_user)

@views.route('/marketplace')
@login_required
def marketplace():
    return render_template("marketplace.html", user=current_user)

@views.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
    
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_size = request.form.get('item_size')
        item_type = request.form.get('item_type')
        has_tag = request.form.get('tag')
        desc = request.form.get('desc')
        condition = request.form.get('condition')
        active = true
        completed = false

        if len(item_name) < 2:
            flash('Email must be greater than 3 characters.', category='error')
        elif item_size == "":
            flash('Please Select a Item size', category='error')
        elif item_type == "":
            flash('Please Select a item type', category='error')
        elif has_tag == "":
            flash('Please Select a tag status', category='error')
        elif len(desc) < 10:
            flash('Description is too short', category='error')
        elif condition == "":
            flash('Please select a condition', category='error')
        else:
            active_trades = True
            completed = False
            new_trade = Trades(item_name=item_name, size=item_size, item_type=item_type, desc = desc, condition=condition,tag=has_tag, active_trade = active_trades, completed = completed, user_id=current_user.id)
            db.session.add(new_trade)
            db.session.commit()
            flash('Trade Created!', category='success')
            return redirect(url_for('views.userpage'))           
    total_trades = get_num_trades(current_user)
    active_trades = get_active_trades(current_user)
    return render_template("userpage.html", user=current_user, total_trades =total_trades, active_trades = active_trades)

@views.route('/usersettings',methods=['GET', 'POST'])
@login_required
def usersettings():
    return render_template("usersettings.html", user=current_user)

@views.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_size = request.form.get('item_size')
        item_type = request.form.get('item_type')
        has_tag = request.form.get('tag')
        desc = request.form.get('desc')
        condition = request.form.get('condition')
        active = true
        completed = false
        if len(item_name) < 2:
            flash('Email must be greater than 3 characters.', category='error')
        elif item_size == "":
            flash('Please Select a Item size', category='error')
        elif item_type == "":
            flash('Please Select a item type', category='error')
        elif has_tag == "":
            flash('Please Select a tag status', category='error')
        elif len(desc) < 10:
            flash('Description is too short', category='error')
        elif condition == "":
            flash('Please select a condition', category='error')
        else:
            active_trades = True
            completed = False
            new_trade = Trades(item_name=item_name, size=item_size, item_type=item_type, desc = desc, condition=condition,tag=has_tag, active_trade = active_trades, completed = completed, user_id=current_user.id)
            db.session.add(new_trade)
            db.session.commit()
            flash('Trade Created!', category='success')
            return redirect(url_for('views.userpage'))           
    return render_template("create.html",user=current_user)