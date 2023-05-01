from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length

class createRecipeForm(FlaskForm):
    """
    A form used for creating a new recipe. Inherits from FlaskForm.

    Attributes:
        title (StringField): A required StringField for the recipe title.
        servings (IntegerField): A required IntegerField for the recipe servings.
        prep_time (IntegerField): A required IntegerField for the recipe preparation time.
        cook_time (IntegerField): A required IntegerField for the recipe cooking time.
        description (TextAreaField): A required TextAreaField for the recipe description.
        ingredients (StringField): A required StringField for the recipe ingredients.
        instructions (TextAreaField): A required TextAreaField for the recipe instructions.
        submit (SubmitField): A SubmitField for submitting the form.
    """
    title = StringField('Recipe Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (in minutes)', validators=[DataRequired()])
    cook_time = IntegerField('Cooking Time (in minutes)',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Create Recipe')

class editRecipeForm(FlaskForm):
    """
    A form used for editing an existing recipe. Inherits from FlaskForm.

    Attributes:
        title (StringField): A required StringField for the recipe title.
        servings (IntegerField): A required IntegerField for the recipe servings.
        prep_time (IntegerField): A required IntegerField for the recipe preparation time.
        cook_time (IntegerField): A required IntegerField for the recipe cooking time.
        description (TextAreaField): A required TextAreaField for the recipe description.
        ingredients (StringField): A required StringField for the recipe ingredients.
        instructions (TextAreaField): A required TextAreaField for the recipe instructions.
        recipe_id (HiddenField): A HiddenField to store the recipe ID.
        submit (SubmitField): A SubmitField for submitting the form.
    """
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
    """
    A form used for adding or removing tags from a recipe. Inherits from FlaskForm.

    Attributes:
        tags (StringField): A StringField for the recipe tags.
        recipe_id (HiddenField): A HiddenField to store the recipe ID.
        submit_add (SubmitField): A SubmitField for adding tags.
        submit_remove (SubmitField): A SubmitField for removing tags.
    """
    tags = StringField('Tags', validators=[DataRequired(), Length(max=50)])
    recipe_id = HiddenField('Recipe ID')
    submit_add = SubmitField('Add Tag')
    submit_remove = SubmitField('Remove Tag')
