from flask import Blueprint, render_template, request, flash, jsonify, Flask, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .forms import createRecipeForm, editRecipeForm, TagForm
from .models import Recipe, User, Ingredient, Instruction, Tags, Comments, Favorites
from sqlalchemy import asc, desc

# Create a Blueprint object to register views with
views = Blueprint('views', __name__)

# Define a route for the homepage


@views.route('/', methods=['GET', 'POST'])
def home():
    # Get all recipes from the database
    recipes = Recipe.query.all()
    # Render the home page template with the current user and all recipes
    return render_template("home.html", user=current_user, recipes=recipes)

# Define a route for the user page


@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    # Get the current user
    user = current_user
    # Get all recipes created by the current user from the database
    user_recipes = Recipe.query.filter_by(user_id=user.id).all()
    # Render the user page template with the current user and their recipes
    return render_template("user.html", user=user, user_recipes=user_recipes)

# Define a route for the admin page


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # Get the current user
    user = current_user
    # Get all recipes that have been flagged by moderators from the database
    flagged_recipes = Recipe.query.filter(
        Recipe.tags.any(Tags.text == 'FLAGGED')).all()
    # Render the admin page template with the current user and flagged recipes
    return render_template("admin.html", user=user, flagged_recipes=flagged_recipes)

# Define a route for the create recipe page


@views.route('/createRecipe', methods=['GET', 'POST'])
@login_required
def createRecipe():
    # Create a form to create a recipe
    form = createRecipeForm()

    if form.validate_on_submit():
        # Create a new recipe object with data from the form
        recipe = Recipe(user_id=current_user.id,
                        title=form.title.data,
                        description=form.description.data,
                        servings=form.servings.data,
                        prep_time=form.prep_time.data,
                        cook_time=form.cook_time.data,
                        likes=0)
        # Add a 'FLAGGED' tag to the recipe by default
        recipe.tags.append(Tags(text="FLAGGED"))

        # Create and add ingredients to the recipe
        for ingredient_text in request.form.getlist('ingredients'):
            ingredient = Ingredient(text=ingredient_text, recipe=recipe)
            db.session.add(ingredient)

        # Create and add instructions to the recipe
        for instruction_text in request.form.getlist('instructions'):
            instruction = Instruction(text=instruction_text, recipe=recipe)
            db.session.add(instruction)

        # Add the new recipe to the database
        db.session.add(recipe)
        db.session.commit()

        # Flash a success message and redirect the user to their user page
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('views.user'))

    # Render the create recipe page template with the form and the current user
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
    # create a new instance of the TagForm class
    form = TagForm()

    # check if the form data is valid
    if form.validate_on_submit():
        # retrieve the recipe with the specified ID
        recipe = Recipe.query.get_or_404(recipe_id)
        # create a new tag and associate it with the recipe
        tag = Tags(text=form.tags.data, recipe_id=recipe_id)
        # add the tag to the database session and commit the changes
        db.session.add(tag)
        db.session.commit()
        # display a success message using the Flash function
        flash(f'Tag "{tag.text}" has been added to the recipe.')
    else:
        # display an error message using the Flash function if form data is invalid
        flash('Error adding tag. Please try again.', 'danger')

    # redirect the user to the recipe page
    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/remove_tag/<int:tag_id>', methods=['POST'])
@login_required
def remove_tag(recipe_id, tag_id):
    # retrieve the tag with the specified ID
    tag = Tags.query.get_or_404(tag_id)
    # delete the tag from the database session and commit the changes
    db.session.delete(tag)
    db.session.commit()
    # display a success message using the Flash function
    flash('Tag removed successfully!', 'success')
    # redirect the user to the recipe page
    return redirect(url_for('views.recipe', recipe_id=recipe_id))


@views.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    # retrieve the recipe with the specified ID
    recipe = Recipe.query.get_or_404(recipe_id)
    # delete the recipe from the database session and commit the changes
    db.session.delete(recipe)
    db.session.commit()
    # display a success message using the Flash function
    flash('Your recipe has been deleted!', 'success')
    # redirect the user to the home page
    return redirect(url_for('views.home'))


@views.route('/recipes/<int:recipe_id>/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def deleteComment(recipe_id, comment_id):
    # retrieve the comment with the specified ID
    comment = Comments.query.get_or_404(comment_id)
    # delete the comment from the database session and commit the changes
    db.session.delete(comment)
    db.session.commit()
    # display a success message using the Flash function
    flash('Your comment has been deleted.', 'success')
    # redirect the user to the recipe page
    return redirect(url_for('views.recipe', recipe_id=recipe_id))


# This view handles editing a recipe
@views.route('/editRecipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def editRecipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = editRecipeForm()

    if form.validate_on_submit():
        # Update the recipe data
        recipe.title = form.title.data
        print(f"Form title: {form.title.data}")
        recipe.description = form.description.data
        recipe.servings = form.servings.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data

        # Delete the old ingredients and instructions
        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        Instruction.query.filter_by(recipe_id=recipe.id).delete()

        # Add the new ingredients and instructions
        for i, ingredient_text in enumerate(request.form.getlist('ingredients')):
            ingredient = Ingredient(text=ingredient_text, recipe=recipe)
            db.session.add(ingredient)

        for i, instruction_text in enumerate(request.form.getlist('instructions')):
            instruction = Instruction(text=instruction_text, recipe=recipe)
            db.session.add(instruction)

        # Commit the changes
        db.session.commit()

        flash('Recipe edited successfully!', 'success')
        return redirect(url_for('views.recipe', recipe_id=recipe.id))

    form.title.data = recipe.title
    form.description.data = recipe.description
    form.servings.data = recipe.servings
    form.prep_time.data = recipe.prep_time
    form.cook_time.data = recipe.cook_time

    # Fetch the existing ingredients and instructions
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    instructions = Instruction.query.filter_by(recipe_id=recipe_id).all()

    return render_template('editRecipe.html', title='Edit Recipe', recipe_id=recipe_id, form=form, user=current_user, ingredients=ingredients, instructions=instructions)


# This view handles filtering the recipe list by tags, search query, and ingredient query
@views.route('/filter', methods=['GET'])
def filter():
    tags = request.args.getlist('tags')
    search_query = request.args.get('search')
    ingredient_query = request.args.get('ingredient_search')

    if search_query and not ingredient_query:
        filtered_recipes = Recipe.query.filter(
            Recipe.title.ilike(f'%{search_query}%'))
    elif ingredient_query and not search_query:
        filtered_recipes = Recipe.query.join(Recipe.ingredients).filter(
            Ingredient.text.ilike(f'%{ingredient_query}%'))
    elif search_query and ingredient_query:
        filtered_recipes = Recipe.query.filter(Recipe.title.ilike(f'%{search_query}%')).join(
            Recipe.ingredients).filter(Ingredient.text.ilike(f'%{ingredient_query}%'))
    else:
        filtered_recipes = Recipe.query

    if tags:
        filtered_recipes = filtered_recipes.join(
            Recipe.tags).filter(Tags.text.in_(tags))

    filtered_recipes = filtered_recipes.all()
    user = current_user
    return render_template('recipes.html', recipes=filtered_recipes, user=user)


# This view handles sorting the recipe list by various options
@views.route('/recipes/sort', methods=['GET'])
@login_required
def sort_recipes():
    option = request.args.get('sort_option')
    search_query = request.args.get('search', '')

    if option == 'title_asc':
        sorted_recipes = Recipe.query.order_by(asc(Recipe.title)).all()
    elif option == 'title_desc':
        sorted_recipes = Recipe.query.order_by(desc(Recipe.title)).all()
    elif option == 'likes_asc':
        sorted_recipes = Recipe.query.order_by(asc(Recipe.likes)).all()
    elif option == 'likes_desc':
        sorted_recipes = Recipe.query.order_by(desc(Recipe.likes)).all()
    else:
        # sort by number of likes in ascending order by default
        sorted_recipes = Recipe.query.order_by(asc(Recipe.likes)).all()

    # filter by search query
    if search_query:
        sorted_recipes = [
            recipe for recipe in sorted_recipes if search_query.lower() in recipe.title.lower()]

    # check if user is authenticated to show liked recipes
    user = current_user
    if user.is_authenticated:
        liked_recipes = [like.recipe_id for like in user.likes]
    for recipe in sorted_recipes:
        if recipe.id in liked_recipes:
            recipe.liked = True
    else:
        liked_recipes = []

    return render_template('recipes.html', recipes=sorted_recipes, search_query=search_query, liked_recipes=liked_recipes, user=user)
