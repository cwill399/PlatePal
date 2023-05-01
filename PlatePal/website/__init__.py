from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from config import Config, TestConfig

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Define the name of the database file
DB_NAME = "database.db"

# Define a function to create the Flask application instance
def create_app():

    # Create a new Flask application instance
    app = Flask(__name__)

    # Configure the app's secret key
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    # Configure the app's database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the app's SQLAlchemy instance with the app
    db.init_app(app)

    # Import the views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the views and auth blueprints with the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the User model
    from .models import User

    # Create the database tables based on the defined models
    with app.app_context():
        db.create_all()

    # Initialize the LoginManager instance
    login_manager = LoginManager()

    # Set the login view to the 'auth.login' endpoint
    login_manager.login_view = 'auth.login'

    # Initialize the LoginManager with the app
    login_manager.init_app(app)

    # Define the user_loader callback for the LoginManager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the fully-configured Flask application instance
    return app

# Define a function to create the database
def create_database(app):

    # Check if the database file already exists
    if not path.exists('website/' + DB_NAME):

        # If the database file does not exist, create it
        db.create_all(app=app)

        # Print a message indicating that the database has been created
        print('Created Database!')

def create_test_app(config_class=TestConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_test_database(test_app):
    with test_app.app_context():
        db.drop_all()
        db.create_all()
        print('Test database created.')
