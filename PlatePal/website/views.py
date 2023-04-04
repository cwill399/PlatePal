from flask import Blueprint, render_template, request, flash, jsonify, Flask, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .forms import createRecipeForm
from .models import Recipe, User, Ingredient, Instruction

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    recipes = Recipe.query.all()
    return render_template("home.html", user=current_user, recipes=recipes)

@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    user = current_user
    user_recipes = Recipe.query.filter_by(user_id=user.id).all()
    return render_template("user.html", user=user, user_recipes=user_recipes)

@views.route('/createRecipe', methods=['GET', 'POST'])
@login_required
def createRecipe():
    form = createRecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(user_id=current_user.id,
                        title=form.title.data,
                        description=form.description.data,
                        servings=form.servings.data,
                        prep_time=form.prep_time.data,
                        cook_time=form.cook_time.data)
        
        # create and add ingredients to recipe
        for ingredient_text in form.ingredients.data.split('\n'):
            if ingredient_text.strip():
                ingredient = Ingredient(text=ingredient_text.strip())
                recipe.ingredients.append(ingredient)

        # create and add instructions to recipe
        for instruction_text in form.instructions.data.split('\n'):
            if instruction_text.strip():
                instruction = Instruction(text=instruction_text.strip())
                recipe.instructions.append(instruction)

        
        db.session.add(recipe)
        db.session.commit()

        flash('Recipe created successfully!', 'success')
        return redirect(url_for('views.user'))

    return render_template('createRecipe.html', title='Create Recipe', form=form, user=current_user)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/recipe/<int:recipe_id>')
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe.html", recipe=recipe, user=current_user)

@views.route('/recipes', methods=['GET'])
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes, user=current_user)