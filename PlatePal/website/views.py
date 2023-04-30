from flask import Blueprint, render_template, request, flash, jsonify, Flask, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .forms import createRecipeForm, editRecipeForm, TagForm
from .models import Recipe, User, Ingredient, Instruction, Tags, Comments, Favorites

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


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user = current_user
    flagged_recipes = Recipe.query.filter(
        Recipe.tags.any(Tags.text == 'FLAGGED')).all()
    return render_template("admin.html", user=user, flagged_recipes=flagged_recipes)


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
                        cook_time=form.cook_time.data,
                        likes=0)
        recipe.tags.append(Tags(text="FLAGGED"))

        # create and add ingredients to recipe
        for ingredient_text in request.form.getlist('ingredients'):
            ingredient = Ingredient(text=ingredient_text, recipe=recipe)
            db.session.add(ingredient)

        for instruction_text in request.form.getlist('instructions'):
            instruction = Instruction(text=instruction_text, recipe=recipe)
            db.session.add(instruction)

        db.session.add(recipe)
        db.session.commit()

        flash('Recipe created successfully!', 'success')
        return redirect(url_for('views.user'))

    return render_template('createRecipe.html', title='Create Recipe', form=form, user=current_user)


@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)


@views.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    tag_form = TagForm()
    return render_template("recipe.html", recipe=recipe, user=current_user, tag_form=tag_form)


@views.route('/recipes', methods=['GET'])
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes, user=current_user)


@views.route('/recipes/<int:recipe_id>/comments/<int:user_id>', methods=['POST'])
@login_required
def addComment(recipe_id, user_id):
    comment_text = request.form['comment_text']
    recipe = Recipe.query.get_or_404(recipe_id)
    user = User.query.get_or_404(user_id)
    comment = Comments(text=comment_text, recipe=recipe, user=user)
    db.session.add(comment)
    db.session.commit()
    flash('Your comment has been added!', 'success')
    return redirect(url_for('views.recipe', recipe_id=recipe_id))




@views.route('/recipes/<int:recipe_id>/likes', methods=['POST', 'GET'])
@login_required
def likeRecipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if request.form['like'] == 'like':
        recipe.likes += 1
    elif request.form['like'] == 'dislike':
        recipe.likes -= 1

    db.session.commit()

    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/favorite', methods=['POST'])
@login_required
def favorite_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user = current_user

    # Check if the user has already favorited this recipe
    if recipe in user.favorites:
        # Remove favorite
        user.favorites.remove(recipe)
        db.session.commit()
        flash('Recipe unfavorited!', 'success')
    else:
        # Add favorite
        user.favorites.append(recipe)
        db.session.commit()
        flash('Recipe favorited!', 'success')

    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/add_tag', methods=['POST'])
@login_required
def add_tag(recipe_id):
    form = TagForm()

    if form.validate_on_submit():
        recipe = Recipe.query.get_or_404(recipe_id)
        tag = Tags(text=form.tags.data, recipe_id=recipe_id)
        db.session.add(tag)
        db.session.commit()
        flash(f'Tag "{tag.text}" has been added to the recipe.')
    else:
        flash('Error adding tag. Please try again.', 'danger')

    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/remove_tag/<int:tag_id>', methods=['POST'])
@login_required
def remove_tag(recipe_id, tag_id):
    tag = Tags.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag removed successfully!', 'success')
    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('views.home'))

@views.route('/recipes/<int:recipe_id>/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def deleteComment(recipe_id, comment_id):
    comment = Comments.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted.', 'success')
    return redirect(url_for('views.recipe', recipe_id=recipe_id))

@views.route('/editRecipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def editRecipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = editRecipeForm()

    if form.validate_on_submit():
        # update the recipe data
        recipe.title = form.title.data
        print(f"Form title: {form.title.data}")
        recipe.description = form.description.data
        recipe.servings = form.servings.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        
        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        Instruction.query.filter_by(recipe_id=recipe.id).delete()

        # update the ingredients and instructions
        for i, ingredient_text in enumerate(request.form.getlist('ingredients')):
            ingredient = Ingredient(text=ingredient_text, recipe=recipe)
            db.session.add(ingredient)

        for i, instruction_text in enumerate(request.form.getlist('instructions')):
            instruction = Instruction(text=instruction_text, recipe=recipe)
            db.session.add(instruction)

        db.session.commit()

        flash('Recipe edited successfully!', 'success')
        return redirect(url_for('views.recipe', recipe_id=recipe.id))

    form.title.data = recipe.title
    form.description.data = recipe.description
    form.servings.data = recipe.servings
    form.prep_time.data = recipe.prep_time
    form.cook_time.data = recipe.cook_time
    # fetch the existing ingredients and instructions
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    instructions = Instruction.query.filter_by(recipe_id=recipe_id).all()

    return render_template('editRecipe.html', title='Edit Recipe', recipe_id=recipe_id, form=form, user=current_user, ingredients=ingredients, instructions=instructions)

@views.route('/filter', methods=['GET'])
def filter():
    tags = request.args.getlist('tags')
    search_query = request.args.get('search')
    
    if search_query:
        filtered_recipes = Recipe.query.filter(Recipe.title.ilike(f'%{search_query}%'))
    else:
        filtered_recipes = Recipe.query
    
    if tags:
        filtered_recipes = filtered_recipes.join(Recipe.tags).filter(Tags.text.in_(tags))
    
    filtered_recipes = filtered_recipes.all()
    user = current_user
    return render_template('recipes.html', recipes=filtered_recipes, user=user)
