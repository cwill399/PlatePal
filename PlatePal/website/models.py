from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    """
    User model to store user information, and relationships with other models such as Recipe, Like and Favorites
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    favorites = db.relationship('Recipe', secondary='favorites', backref=db.backref(
        'favorited_by', lazy='dynamic'))
    likes = db.relationship('Like', backref='user', lazy=True)

class Like(db.Model):
    """
    Like model to store likes for recipes by users
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class Recipe(db.Model):
    """
    Recipe model to store recipe information, and relationships with other models such as User, Ingredient, Instruction, Tags, Comments and Favorites
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade='all, delete')
    instructions = db.relationship('Instruction', backref='recipe', lazy=True, cascade='all, delete')
    tags = db.relationship('Tags', backref='recipe', lazy=True, cascade='all, delete')
    comments = db.relationship('Comments', backref='recipe', lazy=True, cascade='all, delete-orphan')
    likes = db.Column(db.Integer, default=0)

class Ingredient(db.Model):
    """
    Ingredient model to store ingredients for a recipe
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)

class Instruction(db.Model):
    """
    Instruction model to store instructions for a recipe
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)

class Tags(db.Model):
    """
    Tags model to store tags for a recipe
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64))
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)

class Comments(db.Model):
    """
    Comments model to store comments for a recipe
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='cascade'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

class Favorites(db.Model):
    """
    Favorites model to store which user has favorited which recipe
    """
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

