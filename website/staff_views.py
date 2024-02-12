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


def process_chart_data(data):
    labels = list(data.keys())
    values = list(data.values())

    return {'labels': labels, 'values': values}


@staff_views.route('/user-preferences')
@login_required
def user_preferences():
    users = User.query.all()

    # Fetch user preferences data from the database
    preferences = Preference.query.all()

    # Aggregate data for Top Ingredients, Top Cuisines, and Dietary Restrictions
    top_ingredients_data = aggregate_chart_data(preferences, 'top_preferences')
    top_cuisines_data = aggregate_chart_data(preferences, 'top_cuisines')
    dietary_restrictions_data = aggregate_chart_data(preferences, 'dietary_restrictions')

    # Process data for the template, ensure labels are lists and values are integers
    top_ingredients_data = process_chart_data(top_ingredients_data)
    top_cuisines_data = process_chart_data(top_cuisines_data)
    dietary_restrictions_data = process_chart_data(dietary_restrictions_data)

    return render_template('staff_view_preferences.html', users=users,
                           topIngredientsData=top_ingredients_data,
                           topCuisinesData=top_cuisines_data,
                           dietaryRestrictionsData=dietary_restrictions_data,
                           staff=True)


def aggregate_chart_data(preferences, category):
    data = {}

    for preference in preferences:
        category_value = getattr(preference, category)
        if category_value:
            categories = category_value.split(', ')
            for cat in categories:
                if cat in data:
                    data[cat] += 1
                else:
                    data[cat] = 1
    print(data)
    return data

# ignore this comment