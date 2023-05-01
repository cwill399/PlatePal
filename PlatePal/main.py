# Importing the create_app function from the website module
from website import create_app

# Creating the Flask app instance by calling create_app function
app = create_app()

# Check if this script is being run directly and if so, run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
