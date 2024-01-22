from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from .models import User, Post, Comment, Like, Preference
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re
from .config import SITE_KEY, SECRET_KEY, VERIFY_URL
import requests
from flask_mail import Mail, Message
from random import randint
from validate_email_address import validate_email
from itsdangerous import URLSafeTimedSerializer

auth = Blueprint('auth', __name__)
mail = Mail()

otp = None


@auth.route('/welcome-page', methods=['GET', 'POST'])
def welcome_page():
    return render_template('welcome_page.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global otp

    print(request.form)

    # reCAPTCHA
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()

        print(verify_response)

        if verify_response['success'] == False or verify_response['score'] < 0.5:
            flash('reCAPTCHA verification failed.', category='error')
            return render_template('login.html', user=current_user, site_key=SITE_KEY)

        # checking for valid email format
        if not validate_email(email):
            flash('Invalid email address format.', category='error')
            return render_template('login.html', user=current_user, site_key=SITE_KEY)

        existing_email = User.query.filter_by(email=email).first()

        # logging in user, check for email and password
        if existing_email:
            if check_password_hash(existing_email.password, password):
                flash('Logged in successfully!', category='success')
                login_user(existing_email, remember=True)

                # generate and send OTP via email
                otp = randint(100000, 999999)
                session['otp'] = otp

                send_otp_email(email, otp)

                # redirect to OTP verification page

                return redirect(url_for('views.homepage', email=email))
                # change to this when done
                # return redirect(url_for('auth.verify_otp', email=email))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user, site_key=SITE_KEY)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # checking for valid email format
        if not validate_email(email):
            flash('Invalid email address format.', category='error')
            return render_template('sign_up.html', user=current_user, site_key=SITE_KEY)

        # Check password strength requirements
        errors = []

        if len(password) < 12:
            errors.append('Password must be at least 12 characters long.')

        if not re.search("[A-Z]", password):
            errors.append('Password must include at least one uppercase letter.')

        if not re.search("[a-z]", password):
            errors.append('Password must include at least one lowercase letter.')

        if not re.search("[0-9]", password):
            errors.append('Password must include at least one number.')

        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append('Password must include at least one special character.')

        if errors:
            for error in errors:
                flash(error, category='error')
            return render_template("sign_up.html", user=current_user, site_key=SITE_KEY)

        # reCAPTCHA
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()

        print(verify_response)

        if verify_response['success'] == False or verify_response['score'] < 0.5:
            flash('reCAPTCHA verification failed.', category='error')
            return render_template('sign_up.html', user=current_user, site_key=SITE_KEY)

        # signing up user, check for unique username and email, hash password
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username is already taken.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        else:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(email=email, username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')

                print(request.form)
                print(f"Hashed Password: {hashed_password}")

                # generate and send OTP via email
                otp = randint(100000, 999999)
                session['otp'] = otp

                send_otp_email(email, otp)

                # redirect to OTP verification page

                return redirect(url_for('views.homepage', email=email))
                # change to this when done
                # return redirect(url_for('auth.verify_otp', email=email))
                # add user to database

    return render_template("sign_up.html", user=current_user, site_key=SITE_KEY)


@auth.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    global otp

    # retrieve email from query parameters
    email = request.args.get('email')

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        stored_otp = session.get('otp')

        if stored_otp and int(user_otp) == stored_otp:
            # reset otp
            session.pop('otp', None)

            user = User.query.filter_by(email=email).first()

            if user:
                # Check if preferences are already set for the user
                preferences = Preference.query.filter_by(username=user.username).first()

                if preferences:
                    # If preferences are set, redirect to landing page
                    login_user(user, remember=True)
                    flash('Email verification successful! You are now logged in.', category='success')
                    return redirect(url_for('views.homepage'))
                else:
                    # If preferences are not set, redirect to user preferences form
                    login_user(user, remember=True)
                    flash('Email verification successful! Please set your preferences.', category='success')
                    return redirect(url_for('views.process_preferences'))
            else:
                flash('User not found. Please try again.', category='error')

        else:
            flash('Incorrect OTP. Please try again.', category='error')

    return render_template('verify_otp.html', user=current_user, verifying=True)


def send_otp_email(email, otp):
    msg = Message(subject='Eco-Eats OTP Verification', sender='kathleenchan.wqq@gmail.com', recipients=[email])
    msg.body = 'Your OTP for Eco-Eats: %s' % otp
    mail.send(msg)


@auth.route('/delete-account')
@login_required
def delete_account():
    return render_template('delete_account.html', user=current_user)


@auth.route('/perform-delete-account')
@login_required
def perform_delete_account():
    # Delete user's posts
    posts_to_delete = Post.query.filter_by(author=current_user.username).all()
    for post in posts_to_delete:
        db.session.delete(post)

    # Delete user's comments
    comments_to_delete = Comment.query.filter_by(author=current_user.username).all()
    for comment in comments_to_delete:
        db.session.delete(comment)

    # Delete user's likes
    likes_to_delete = Like.query.filter_by(author=current_user.username).all()
    for like in likes_to_delete:
        db.session.delete(like)

    preferences_to_delete = Preference.query.filter_by(username=current_user.username).all()
    for preference in preferences_to_delete:
        db.session.delete(preference)

    # Delete the user
    db.session.delete(current_user)
    db.session.commit()

    logout_user()

    flash('Account deleted successfully!', category='success')
    return redirect(url_for('views.community_forum'))


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            reset_token = generate_reset_token(user)

            send_password_reset_email(user, reset_token)

            flash('Password reset link has been sent to your email.', category='info')
            return redirect(url_for('auth.login'))

        else:
            flash('Email not found. Please enter the email associated with your account.', category='error')

    return render_template('reset_password_request.html', user=current_user, site_key=SITE_KEY)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = verify_reset_token(token)
    except Exception as e:
        flash('Invalid or expired reset link.', category='error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Invalid or expired reset link.', category='error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')

        # Check password strength requirements
        errors = []

        if len(new_password) < 12:
            errors.append('Password must be at least 12 characters long.')

        if not re.search("[A-Z]", new_password):
            errors.append('Password must include at least one uppercase letter.')

        if not re.search("[a-z]", new_password):
            errors.append('Password must include at least one lowercase letter.')

        if not re.search("[0-9]", new_password):
            errors.append('Password must include at least one number.')

        if not re.search("[!@#$%^&*(),.?\":{}|<>]", new_password):
            errors.append('Password must include at least one special character.')

        if errors:
            for error in errors:
                flash(error, category='error')
            return render_template("reset_password.html", user=current_user, site_key=SITE_KEY, token=token)

        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        user.password = hashed_password
        db.session.commit()

        flash('Password reset successful! You can now log in with your new password.', category='success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', user=current_user, site_key=SITE_KEY, token=token)


def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(user.email, salt='reset-password-salt')


def verify_reset_token(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = s.loads(token, salt='reset-password-salt', max_age=3600)  # Token expires in 1 hour
    return email


def send_password_reset_email(user, token):
    reset_link = url_for('auth.reset_password', token=token, _external=True)
    msg = Message(subject='Eco-Eats Password Reset', sender='kathleenchan.wqq@gmail.com', recipients=[user.email])
    msg.body = f'Click the following link to reset your password: {reset_link}'
    mail.send(msg)


@auth.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_email = request.form.get('new_email')

        # Validate the new username
        if new_username:
            if len(new_username) < 2:
                flash('Username must be greater than 1 character.', category='error')
                return redirect(url_for('auth.update_profile'))

            existing_username = User.query.filter_by(username=new_username).first()
            if existing_username and existing_username != current_user:
                flash('Username is already taken.', category='error')
                return redirect(url_for('auth.update_profile'))

            # Update posts associated with the user's old username
            old_username = current_user.username
            posts_to_update = Post.query.filter_by(author=old_username).all()
            comments_to_update = Comment.query.filter_by(author=old_username).all()
            for post in posts_to_update:
                post.author = new_username

            for comment in comments_to_update:
                comment.author = new_username

            current_user.username = new_username

        # Validate the new email
        if new_email:
            if len(new_email) < 4 or not validate_email(new_email):
                flash('Invalid email address format.', category='error')
                return redirect(url_for('auth.update_profile'))

            existing_email = User.query.filter_by(email=new_email).first()
            if existing_email and existing_email != current_user:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.update_profile'))

            current_user.email = new_email

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.community_forum'))

    return render_template('update_profile.html', user=current_user)

# ignore this comment
