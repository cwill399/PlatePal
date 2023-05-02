from website import create_test_app, db
from website.models import User, Recipe, Instruction, Ingredient, Tags, Comments, Like, Favorites
import pytest, requests
from flask_login import login_user, logout_user, current_user, LoginManager



@pytest.fixture(scope='module')
def test_client():
    flask_app = create_test_app()
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            # Create the database and the database table
            db.create_all()

            # Create a test user
            test_user = User(email='admin@platepal.com', password='testPass', first_name='test')
            db.session.add(test_user)
            db.session.commit()

            # Set up Flask-Login
            login_manager = LoginManager()
            login_manager.init_app(flask_app)
            login_manager.login_view = 'auth.login'

            @login_manager.user_loader
            def load_user(user_id):
                user = User.query.filter_by(id=user_id).first()
                return user

            # Log in the test user
            with testing_client.session_transaction() as session:
                session['_user_id'] = test_user.id
                session['_fresh'] = True

            # Run the tests
            yield testing_client

            # Clean up the database
            db.drop_all()

def test_Views(test_client):
    # Ensure the user is logged in
    with test_client.session_transaction() as session:
        session['_user_id'] = 1
        session['_fresh'] = True

    # Send a POST request to create a new recipe
    instruction1 = Instruction(text='Instruction 1')
    instruction2 = Instruction(text='Instruction 2')
    ingredient1 = Ingredient(text='Ingredient 1')
    ingredient2 = Ingredient(text='Ingredient 2')

    response = test_client.post('/createRecipe', data={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.',
        'servings': '4',
        'prep_time': '30',
        'cook_time': '60',
        'instructions': [instruction1.text, instruction2.text],
        'ingredients': [ingredient1.text, ingredient2.text]
    })
    #Assert that we redirect after creating recipe
    assert response.status_code == 302
    # Ensure the new recipe is added to the database
    recipe = Recipe.query.filter_by(title='Test Recipe').first()
    assert recipe is not None
    assert recipe.description == 'This is a test recipe.'
    assert recipe.servings == 4
    assert recipe.prep_time == 30
    assert recipe.cook_time == 60
    assert len(recipe.ingredients) == 2
    assert len(recipe.instructions) == 2
    assert recipe.ingredients[0].text == 'Ingredient 1'
    assert recipe.ingredients[1].text == 'Ingredient 2'
    assert recipe.instructions[0].text == 'Instruction 1'
    assert recipe.instructions[1].text == 'Instruction 2'
    assert recipe.tags[0].text == "FLAGGED"

     # Get the recipe page
    response = test_client.get(f'/recipe/{recipe.id}')
    assert response.status_code == 200

    # Get the tag ID for the "FLAGGED" tag
    flagged_tag_id = Tags.query.filter_by(text='FLAGGED').first().id
    response = test_client.post(f'/recipe/{recipe.id}/remove_tag/{flagged_tag_id}')
    assert response.status_code == 302
    response = test_client.get(f'/recipe/{recipe.id}')
    recipes = Recipe.query.filter(
        Recipe.tags.any(Tags.text != 'FLAGGED')).all()
    with pytest.raises(IndexError):
        recipes[0].tags[0].text 
    assert response.status_code == 200
    

    #add second recipe for sort and filter function tests laters
    instruction1 = Instruction(text='Instruction 1')
    instruction2 = Instruction(text='Instruction 2')
    ingredient1 = Ingredient(text='Ingredient 1')
    ingredient2 = Ingredient(text='Ingredient 2')

    response = test_client.post('/createRecipe', data={
        'title': 'A Test Recipe',
        'description': 'This is a test recipe.',
        'servings': '4',
        'prep_time': '30',
        'cook_time': '60',
        'instructions': [instruction1.text, instruction2.text],
        'ingredients': [ingredient1.text, ingredient2.text]
    })
    flagged_tag_id = Tags.query.filter_by(text='FLAGGED').first().id
    response = test_client.post(f'/recipe/{recipe.id}/remove_tag/{flagged_tag_id}')


    #Test that we can succesfully search by title
    response = test_client.get('/filter?search=test')
    assert response.status_code == 200
    assert b'Test Recipe' in response.data

    # add the tag to the recipe
    response = test_client.post('/recipe/1/add_tag', data={'tags': 'Test'})
    assert response.status_code == 302  # expect a redirect after adding a tag

    # filter by the tag using the /filter route
    response = test_client.get('/filter?tags=Test')
    assert response.status_code == 200  # expect a successful response
    assert b'Test Recipe' in response.data  # expect to find the test recipe in the filtered results


    response = test_client.get('/recipes', data=recipes)
    assert response.status_code == 200
    assert b"Recipe" in response.data

    #Sort alphabetically ascending
    response = test_client.get('/recipes/sort', query_string={'sort_option': 'title_asc'})
    assert response.status_code == 200
    assert b"A Test Recipe" in response.data
    assert b"Test Recipe" in response.data
    #Assert that T comes before A when ascending
    assert response.data.index(b"A Test Recipe") < response.data.index(b"Test Recipe")
    response = test_client.get('/recipes/sort', query_string={'sort_option': 'title_desc'})
    assert response.status_code == 200
    assert b"A Test Recipe" in response.data
    assert b"Test Recipe" in response.data
    #Assert A comes before T when descending
    assert response.data.index(b"A Test Recipe") > response.data.index(b"Test Recipe")

    response = test_client.post('/recipes/1/likes', data={'like': 'like'})
    assert response.status_code == 302  # should redirect to the recipe page
    recipe = Recipe.query.get(1)
    assert recipe.likes == 1  # should increment the number of likes by 1
    response = test_client.post('/recipes/1/likes', data={'like': 'dislike'})
    assert response.status_code == 302  # should redirect to the recipe page
    recipe = Recipe.query.get(1)
    assert recipe.likes == 0  # should increment the number of likes by 1
    response = test_client.post('/recipes/1/likes', data={'like': 'like'})

    response = test_client.get('/recipes/sort?sort_option=likes_desc')
    assert response.status_code == 200
    # Assert that the recipe with the most likes is displayed first
    assert b'A Test Recipe' in response.data
    assert b'Test Recipe' in response.data
    assert response.data.index(b'A Test Recipe') > response.data.index(b'Test Recipe')
    response = test_client.get('/recipes/sort?sort_option=likes_asc')
    assert response.status_code == 200
    # Assert that the recipe with the most likes is displayed first
    assert b'A Test Recipe' in response.data
    assert b'Test Recipe' in response.data
    assert response.data.index(b'A Test Recipe') < response.data.index(b'Test Recipe')


    response = test_client.get('/recipe/{}'.format(recipe.id))
    # Check that the response is successful and contains the recipe title
    assert response.status_code == 200
    assert b"Test Recipe" in response.data


    """Tests below assert the urls are viewable"""
    response = test_client.get('/user')
    assert response.status_code == 200
    assert b"User" in response.data
    assert b"Welcome" in response.data
    assert b"admin" in response.data
    assert b"Test Recipe" in response.data

    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"Featured Recipes" in response.data
    assert b"Plate Pal" in response.data

    response = test_client.get('/sign-up')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

    response = test_client.get('/about')
    assert response.status_code == 200
    assert b"About" in response.data







