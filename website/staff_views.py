from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Preference
from . import db

staff_views = Blueprint('staff_views', __name__)


@staff_views.route('/user-accounts')
@login_required
def dashboard():

    users = User.query.all()

    return render_template('staff_view_accounts.html', users=users, staff=True)


@staff_views.route('/user-preferences')
@login_required
def user_preferences():

    users = User.query.all()
    preferences = Preference.query.all()

    return render_template('staff_view_preferences.html', users=users, preferences=preferences, staff=True)
