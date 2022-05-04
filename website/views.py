from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from sqlalchemy import false, true
from werkzeug.security import generate_password_hash, check_password_hash

from website.dbfunc import get_active_trades, get_num_trades
from src.models import Notes
from src.models import Users
from src.models import Trades
from src.models import db
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
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
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            
    return render_template("trade.html", user=current_user)

@views.route('/createtrade', methods=['GET', 'POST'])
@login_required
def createtrade():
    if request.method == 'POST':
        pass
        '''''
        if len() < 1:
            pass
        else:
            pass
        '''''
    return render_template("create.html", user=current_user)


@views.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
    return render_template("userpage.html", user=current_user)

@views.route('/usersettings',methods=['GET', 'POST'])
@login_required
def usersettings():
    return render_template("usersettings.html", user=current_user)