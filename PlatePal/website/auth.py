# Import necessary modules
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the 'db' object from the '__init__.py' file
from flask_login import login_user, login_required, logout_user, current_user

# Create a new blueprint object for authentication routes
auth = Blueprint('auth', __name__)

# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if a user with the provided email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Verify the provided password matches the password hash in the database
            if check_password_hash(user.password, password):
                # If password is correct, log the user in, and redirect to the home page
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                # If password is incorrect, flash an error message
                flash('Incorrect password, try again.', category='error')
        else:
            # If the email doesn't exist, flash an error message
            flash('Email does not exist.', category='error')

    # Render the login page template with the current user object
    return render_template("login.html", user=current_user)

# Route for logout
@auth.route('/logout')
@login_required
def logout():
    # Log the user out and redirect to the login page
    logout_user()
    return redirect(url_for('auth.login'))

# Route for sign up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # If the email already exists, flash an error message
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            # If email length is less than 4, flash an error message
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            # If first name length is less than 2, flash an error message
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            # If passwords don't match, flash an error message
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            # If password length is less than 7, flash an error message
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user with the provided information and commit to the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # Log the new user in and redirect to the home page
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
