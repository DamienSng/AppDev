from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, Preference
from . import db
import openpyxl
from fuzzywuzzy import fuzz
from .Kforms import UserPreferencesForm

views = Blueprint('views', __name__)


@views.route('/landing-page', methods=['GET', 'POST'])
@login_required
def landing_page():
    # Fetch user preferences from the database
    username = current_user.username
    recipes = get_recommendations(username)

    return render_template('landing_page.html', recipes=recipes)


@views.route('/process-preferences', methods=['POST', 'GET'])
@login_required
def process_preferences():
    if request.method == 'POST':
        # Process preferences directly without using a form
        username = current_user.username
        top_preferences = request.form.getlist('top_preferences')
        top_cuisines = request.form.getlist('top_cuisines')
        dietary_restrictions = request.form.get('dietary_restrictions')

        # Validate the form inputs
        if not top_preferences:
            flash('Please choose at least one checkbox for Top 3 Ingredients.', 'error')
            return redirect(url_for('views.process_preferences'))

        if not top_cuisines:
            flash('Please choose at least one checkbox for Top 3 Cuisines.', 'error')
            return redirect(url_for('views.process_preferences'))

        if len(top_preferences) > 3:
            flash('Please choose a maximum of 3 checkboxes for Top 3 Ingredients.', 'error')
            return redirect(url_for('views.process_preferences'))

        if len(top_cuisines) > 3:
            flash('Please choose a maximum of 3 checkboxes for Top 3 Cuisines.', 'error')
            return redirect(url_for('views.process_preferences'))

        # Store preferences in the database
        preferences = Preference.query.filter_by(username=username).first()
        if preferences is None:
            preferences = Preference(username=username)

        preferences.top_preferences = ', '.join(top_preferences)
        preferences.top_cuisines = ', '.join(top_cuisines)
        preferences.dietary_restrictions = dietary_restrictions

        db.session.add(preferences)
        db.session.commit()

        flash('Preferences updated successfully.', 'success')
        return redirect(url_for('views.landing_page'))

    return render_template('preferences_form.html')


def get_recommendations(username):
    preferences = Preference.query.filter_by(username=username).first()

    recipes_based_on_preferences = []
    recipes_based_on_cuisines = []

    if preferences:
        top_preferences = preferences.top_preferences.split(', ')
        recipes_based_on_preferences = get_recipes_based_on_preferences(top_preferences)

    if preferences:
        top_cuisines = preferences.top_cuisines.split(', ')
        recipes_based_on_cuisines = get_recipes_based_on_cuisines(top_cuisines)

    # Combine the results
    recipes = recipes_based_on_preferences + recipes_based_on_cuisines

    recommended_recipe = []

    for i in recipes:
        if i not in recommended_recipe:
            recommended_recipe.append(i)
    print(recommended_recipe)

    return recommended_recipe


def get_recipes_based_on_preferences(top_preferences):
    all_recipes = read_recipes_from_excel()

    # Threshold for fuzzy matching
    threshold = 80

    matched_recipes = []
    for recipe in all_recipes:
        recipe_ingredients = recipe['ingredients']
        for preference in top_preferences:
            # Check if any ingredient in the recipe is similar to the preference
            if any(fuzz.partial_ratio(preference, ingredient) >= threshold for ingredient in recipe_ingredients):
                matched_recipes.append(recipe)
                break  # Break out of the inner loop if a match is found

    return matched_recipes


def get_recipes_based_on_cuisines(top_cuisines):
    all_recipes = read_recipes_from_excel()

    # Threshold for fuzzy matching
    threshold = 80

    matched_recipes = []
    for recipe in all_recipes:
        recipe_cuisine = recipe['cuisine']
        for cuisine in top_cuisines:
            # Check if the cuisine in the recipe is similar to the preference
            if fuzz.partial_ratio(cuisine, recipe_cuisine) >= threshold:
                matched_recipes.append(recipe)
                break  # Break out of the inner loop if a match is found

    return matched_recipes


def read_recipes_from_excel(file_path='website/DB.xlsx'):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.worksheets[0]  # Get the first sheet

    recipes = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        recipe = {
            'ID': row[0],
            'Title': row[1],
            'cuisine': row[2],
            'Skill': row[3],
            'Time': row[4],
            'Instruction': row[5],
            'ingredients': row[6].split(', '),  # Split ingredients based on comma
            'Alt': row[7],
            'Optional': row[8],
            'Image': row[9]

        }
        recipes.append(recipe)

    return recipes


@views.route('/community-forum')
@login_required
def community_forum():
    posts = Post.query.all()

    return render_template("community_forum.html", user=current_user, posts=posts)


@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.username != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.community_forum'))


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if not title:
            flash('Title cannot be empty', category='error')
        elif not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=title, text=text, author=current_user.username)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.community_forum'))

    return render_template('create_post.html', user=current_user)


@views.route('/posts/<username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.community_forum'))

    posts = user.posts

    return render_template("user_posts.html", user=current_user, posts=posts, username=username)


@views.route('/create-comment/<post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.username, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='erorr')

    return redirect(url_for('views.community_forum'))


@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.username != comment.author and current_user.username != comment.post.author:
        flash('You do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.community_forum'))


@views.route('/like-post/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.username, post_id=post_id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.username, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.community_forum'))

# ignore this comment
