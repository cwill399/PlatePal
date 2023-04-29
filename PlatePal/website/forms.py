from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length

class createRecipeForm(FlaskForm):

    title = StringField('Recipe Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (in minutes)', validators=[DataRequired()])
    cook_time = IntegerField('Cooking Time (in minutes)',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Create Recipe')

class editRecipeForm(FlaskForm):
    title = StringField('Recipe Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (in minutes)', validators=[DataRequired()])
    cook_time = IntegerField('Cooking Time (in minutes)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    recipe_id = HiddenField()
    submit = SubmitField('Update Recipe')


class TagForm(FlaskForm):
    tags = StringField('Tags', validators=[DataRequired(), Length(max=50)])
    recipe_id = HiddenField('Recipe ID')
    submit_add = SubmitField('Add Tag')
    submit_remove = SubmitField('Remove Tag')
