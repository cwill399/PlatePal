from website import create_app
from website.models import User

testUser = User(email='test@test.com', password='testPass', first_name='test')
def testHomePage():
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Home" in response.data
        assert b"Featured Recipes" in response.data

def testRecipePage():
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.get('/recipes')
        assert response.status_code == 200
        assert b"Recipes" in response.data

def testSignUpPage():
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.get('/sign-up')
        assert response.status_code == 200
        assert b"Sign Up" in response.data

def testLoginPage():
    flask_app= create_app()
    with flask_app.test_client() as test_client:
        response= test_client.get('/login')
        assert response.status_code == 200




