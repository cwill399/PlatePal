from website.models import User, Recipe

def test_new_user():
    user = User(email='test@test.com', password='testPass', first_name='test')
    assert user.email == 'test@test.com'
    assert user.password == 'testPass'
    assert user.first_name == 'test'

def test_Recipe():
    recipe = Recipe(id=1, user_id=1, title='test title', 
                  description='test description', servings=1, prep_time=1,
                  cook_time=1
                  )
    assert recipe.id == 1
    assert recipe.user_id == 1
    assert recipe.title == "test title"
    assert recipe.description == 'test description'
    assert recipe.servings == 1
    assert recipe.prep_time == 1
    assert recipe.cook_time == 1
