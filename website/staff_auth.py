from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from .models import Staff
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

staff_auth = Blueprint('staff_auth', __name__)
mail = Mail()

otp = None


@staff_auth.route('/staff-login', methods=['GET', 'POST'])
def staff_login():
    global otp

    print(request.form)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()

        print(verify_response)

        if verify_response['success'] == False or verify_response['score'] < 0.5:
            flash('reCAPTCHA verification failed.', category='error')
            return render_template('staff_login.html', user=current_user, site_key=SITE_KEY)

        # checking for valid email format
        if not validate_email(email):
            flash('Invalid email address format.', category='error')
            return render_template('staff_login.html', user=current_user, site_key=SITE_KEY)

        existing_email = Staff.query.filter_by(email=email).first()

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
                return redirect(url_for('staff_auth.verify_otp', email=email))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("staff_login.html", user=current_user, site_key=SITE_KEY)


@staff_auth.route('/staff-logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('staff_auth.staff_login'))


@staff_auth.route('/staff-sign-up', methods=['GET', 'POST'])
def staff_sign_up():
    global otp

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # check for valid email format
        if not validate_email(email):
            flash('Invalid email address format.', category='error')
            return render_template('staff_sign_up.html', user=current_user, site_key=SITE_KEY)

        # check password requirements
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
            return render_template("staff_sign_up.html", user=current_user, site_key=SITE_KEY)

        # reCAPTCHA
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()

        print(verify_response)

        if verify_response['success'] == False or verify_response['score'] < 0.5:
            flash('reCAPTCHA verification failed.', category='error')
            return render_template('staff_sign_up.html', user=current_user, site_key=SITE_KEY)

        # signing up user, check for unique username and email, hash password
        existing_username = Staff.query.filter_by(username=username).first()
        if existing_username:
            flash('Username is already taken.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        else:
            existing_email = Staff.query.filter_by(email=email).first()
            if existing_email:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = Staff(email=email, username=username, password=hashed_password)
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
                return redirect(url_for('staff_auth.verify_otp', email=email))
                # add user to database

    return render_template("staff_sign_up.html", user=current_user, site_key=SITE_KEY)


@staff_auth.route('/staff-verify_otp', methods=['GET', 'POST'])
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

            staff = Staff.query.filter_by(email=email).first()

            if staff:
                login_user(staff, remember=True)
                flash('Email verification successful! You are now logged in.', category='success')
                return redirect(url_for('staff_views.dashboard'))
            else:
                flash('User not found. Please try again.', category='error')

        else:
            flash('Incorrect OTP. Please try again.', category='error')

    return render_template('verify_otp.html', user=current_user, verifying=True, staff=True)


def send_otp_email(email, otp):
    msg = Message(subject='Eco-Eats OTP Verification', sender='kathleenchan.wqq@gmail.com', recipients=[email])
    msg.body = 'Your OTP for Eco-Eats: %s' % otp
    mail.send(msg)


@staff_auth.route('/staff-delete-account')
@login_required
def delete_account():
    return render_template('delete_account.html', user=current_user, staff=True)


@staff_auth.route('/staff-perform-delete-account')
@login_required
def perform_delete_account():
    db.session.delete(current_user)
    db.session.commit()

    logout_user()

    flash('Account deleted successfully!', category='success')
    return redirect(url_for('staff_auth.login'))


@staff_auth.route('/staff-reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        staff = Staff.query.filter_by(email=email).first()

        if staff:
            reset_token = generate_reset_token(staff)

            send_password_reset_email(staff, reset_token)

            flash('Password reset link has been sent to your email.', category='info')
            return redirect(url_for('staff_auth.login'))

        else:
            flash('Email not found. Please enter the email associated with your account.', category='error')

    return render_template('reset_password_request.html', user=current_user, site_key=SITE_KEY)


@staff_auth.route('/staff-reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = verify_reset_token(token)
    except Exception as e:
        flash('Invalid or expired reset link.', category='error')
        return redirect(url_for('staff_auth.login'))

    staff = Staff.query.filter_by(email=email).first()

    if not staff:
        flash('Invalid or expired reset link.', category='error')
        return redirect(url_for('staff_auth.login'))

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
        staff.password = hashed_password
        db.session.commit()

        flash('Password reset successful! You can now log in with your new password.', category='success')
        return redirect(url_for('staff_auth.login'))

    return render_template('reset_password.html', user=current_user, site_key=SITE_KEY, token=token)


def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(user.email, salt='reset-password-salt')


def verify_reset_token(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = s.loads(token, salt='reset-password-salt', max_age=3600)  # Token expires in 1 hour
    return email


def send_password_reset_email(user, token):
    reset_link = url_for('staff_auth.reset_password', token=token, _external=True)
    msg = Message(subject='Eco-Eats Password Reset', sender='kathleenchan.wqq@gmail.com', recipients=[user.email])
    msg.body = f'Click the following link to reset your password: {reset_link}'
    mail.send(msg)


@staff_auth.route('/staff-update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_email = request.form.get('new_email')

        # Validate the new username
        if new_username:
            if len(new_username) < 2:
                flash('Username must be greater than 1 character.', category='error')
                return redirect(url_for('staff_auth.update_profile'))

            existing_username = Staff.query.filter_by(username=new_username).first()
            if existing_username and existing_username != current_user:
                flash('Username is already taken.', category='error')
                return redirect(url_for('staff_auth.update_profile'))

            current_user.username = new_username

        # Validate the new email
        if new_email:
            if len(new_email) < 4 or not validate_email(new_email):
                flash('Invalid email address format.', category='error')
                return redirect(url_for('staff_auth.update_profile'))

            existing_email = Staff.query.filter_by(email=new_email).first()
            if existing_email and existing_email != current_user:
                flash('Email already exists.', category='error')
                return redirect(url_for('staff_auth.update_profile'))

            current_user.email = new_email

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('staff_views.staff_dashboard'))

    return render_template('update_profile.html', user=current_user, staff=True)
