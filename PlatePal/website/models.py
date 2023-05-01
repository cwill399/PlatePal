from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    favorites = db.relationship('Recipe', secondary='favorites', backref=db.backref(
        'favorited_by', lazy='dynamic'))
    likes = db.relationship('Like', backref='user', lazy=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class Recipe(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64))
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='cascade'), nullable=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='cascade'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
