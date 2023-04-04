
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class createRecipeForm(FlaskForm):

    title = StringField('Recipe Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (in minutes)', validators=[DataRequired()])
    cook_time = IntegerField('Cooking Time (in minutes)',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Create Recipe')
