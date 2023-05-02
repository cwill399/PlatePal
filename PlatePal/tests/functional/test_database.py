from website import create_test_app, create_test_database
from website.models import User, Recipe, Ingredient, Instruction, Comments, Tags
import unittest

"""
This test class is testing the interaction between the application and the database, we will create a test User class and a test Recipe class and 
add these to the test database. We will then assert that the User and Recipe class retrived from the database match the values assigned those objects
before being added to the database.
"""

class TestDatabase(unittest.TestCase):
    #setUp and tearDown set up a test database and test client for testing, then clears the test database when done
    def setUp(self):
        self.app = create_test_app()
        create_test_database(self.app)
    def tearDown(self):
        with self.app.app_context():
            from website import db
            db.session.remove()
            db.drop_all()
            print('Test database dropped.')
    
    #creates and adds a user to database, then retrieves and makes sure values for the user are correct.
    def testUser(self):
        testUser = User(id=1,email='test@test.com',password='testPassword',first_name='test')
        with self.app.app_context():
            from website import db
            db.session.add(testUser)
            db.session.commit()
            retrievedUser = User.query.filter_by(email='test@test.com').first()
            assert retrievedUser.id == testUser.id
            assert retrievedUser.email == testUser.email
            assert retrievedUser.password == testUser.password
            assert retrievedUser.first_name == testUser.first_name

    #creates and adds a recipe to database, then retrieves and makes sure values for the recipe are correct.
    def testRecipe(self):
        with self.app.app_context():
            from website import db
            #A recipe needs a user associated it with it so we make a user and add to the database
            user = User(id=1, email='test@test.com', password='testPassword', first_name='test')
            db.session.add(user)
            db.session.commit()
            #Creating and adding the recipe
            recipe = Recipe(user_id=1, title='Test Recipe', description='Test description',
                            servings=4, prep_time=10, cook_time=20)
            db.session.add(recipe)
            db.session.commit()
            #adding test ingredients
            ingredient1 = Ingredient(text='Ingredient 1', recipe_id=recipe.id)
            ingredient2 = Ingredient(text='Ingredient 2', recipe_id=recipe.id)
            db.session.add_all([ingredient1, ingredient2])
            db.session.commit()
            #adding test instructions
            instruction1 = Instruction(text='Instruction 1', recipe_id=recipe.id)
            instruction2 = Instruction(text='Instruction 2', recipe_id=recipe.id)
            db.session.add_all([instruction1, instruction2])
            db.session.commit()
            #add a test tag
            tag = Tags(text='Tag 1', recipe_id=recipe.id)
            db.session.add(tag)
            db.session.commit()
            #add a test comment
            comment = Comments(text='Test comment', recipe_id=recipe.id, user_id=user.id)
            db.session.add(comment)
            db.session.commit()
            #retrieve recipe from test database
            recipe_from_db = Recipe.query.filter_by(id=recipe.id).first()
            #assert all the values of the test recipe are correct.
            assert recipe_from_db.title == 'Test Recipe'
            assert recipe_from_db.description == 'Test description'
            assert recipe_from_db.servings == 4
            assert recipe_from_db.prep_time == 10
            assert recipe_from_db.cook_time == 20
            assert len(recipe_from_db.ingredients) == 2
            assert recipe_from_db.ingredients[0].text == 'Ingredient 1'
            assert recipe_from_db.ingredients[1].text == 'Ingredient 2'
            assert len(recipe_from_db.instructions) == 2
            assert recipe_from_db.instructions[0].text == 'Instruction 1'
            assert recipe_from_db.instructions[1].text == 'Instruction 2'
            assert len(recipe_from_db.tags) == 1
            assert recipe_from_db.tags[0].text == 'Tag 1'
            assert len(recipe_from_db.comments) == 1
            assert recipe_from_db.comments[0].text == 'Test comment'
            assert recipe_from_db.likes == 0

    #testing that when a recipe is deleted, it is no longer in the database
    def testDeleteRecipe(self):
        with self.app.app_context():
            from website import db
            user = User(id=1, email='test@test.com', password='testPassword', first_name='test')
            db.session.add(user)
            db.session.commit()
            recipe = Recipe(user_id=1, title='Test Recipe', description='Test description',
                            servings=4, prep_time=10, cook_time=20)
            db.session.add(recipe)
            db.session.commit()
            db.session.delete(recipe)
            db.session.commit()
            recipe_from_db = Recipe.query.filter_by(id=recipe.id).first()
            assert recipe_from_db is None

    #testing that when a tag is deleted, it is no longer in the database
    def test_deleteTag(self):
        with self.app.app_context():
            from website import db
            user = User(id=1, email='test@test.com', password='testPassword', first_name='test')
            db.session.add(user)
            db.session.commit()
            recipe = Recipe(user_id=1, title='Test Recipe', description='Test description',
                            servings=4, prep_time=10, cook_time=20, id=1)
            db.session.add(recipe)
            db.session.commit()
            tag = Tags(text='Test Tag', id=1, recipe_id=1)
            recipe.tags.append(tag)
            db.session.add(tag)
            db.session.commit()
            recipe.tags.remove(tag)
            db.session.commit()
            recipe_from_db = Recipe.query.filter_by(id=recipe.id).first()
            assert tag not in recipe_from_db.tags

    #testing adding a comment to a recipe, retrieving the recipe and checking that the comment exists and asserting its text value is correct
    def test_addComment(self):
        with self.app.app_context():
            from website import db
            user = User(id=1, email='test@test.com', password='testPassword', first_name='test')
            db.session.add(user)
            db.session.commit()
            recipe = Recipe(user_id=1, title='Test Recipe', description='Test description',
                            servings=4, prep_time=10, cook_time=20)
            db.session.add(recipe)
            db.session.commit()
            comment = Comments(text='Test Comment', user_id=1)
            recipe.comments.append(comment)
            db.session.add(comment)
            db.session.commit()
            recipe_from_db = Recipe.query.filter_by(id=recipe.id).first()
            assert comment in recipe_from_db.comments
            assert recipe_from_db.comments[0].text == "Test Comment"

    #testing that when a comment is deleted, it is no longer in the database
    def test_deleteComment(self):
        with self.app.app_context():
            from website import db
            user = User(id=1, email='test@test.com', password='testPassword', first_name='test')
            db.session.add(user)
            db.session.commit()
            recipe = Recipe(user_id=1, title='Test Recipe', description='Test description',
                            servings=4, prep_time=10, cook_time=20)
            db.session.add(recipe)
            db.session.commit()
            comment = Comments(text='Test Comment', user_id=1)
            recipe.comments.append(comment)
            db.session.add(comment)
            db.session.commit()
            recipe.comments.remove(comment)
            db.session.commit()
            recipe_from_db = Recipe.query.filter_by(id=recipe.id).first()
            assert comment not in recipe_from_db.comments

if __name__ == '__main__':
    unittest.main()
