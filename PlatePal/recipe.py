import sqlite3

def time_to_minutes(time_str):
    """Converts a time string in the format 'X hours' or 'X min' to the equivalent number of minutes"""
    if 'hour' in time_str:
        hours, minutes = time_str.split()
        if '.' in hours:
            hours, decimal = hours.split('.')
            minutes = int(decimal) * 6
            hours = int(hours)
        else:
            hours = int(hours)
            minutes = 0
        return hours * 60 + minutes
    elif 'min' in time_str:
        return int(time_str.split()[0])
    else:
        raise ValueError('Invalid time format')

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS recipes''')

cursor.execute('''CREATE TABLE recipes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  recipe_name TEXT,
                  servings INTEGER,
                  prep_time_str INTEGER,
                  cook_time_str INTEGER,
                  description TEXT,
                  ingredients TEXT,
                  instruction TEXT,
                  tags TEXT,
                  likes INTEGER DEFAULT 0,
                  comments TEXT)''')

recipes = [
    {
        'recipe_name': 'Baked Chicken Parmesan',
        'cook_time_str': '45 min',
        'prep_time_str': '15 min',
        'ingredients': ['4 boneless',
                        'skinless chicken breasts',
                        'Salt and freshly ground black pepper',
                        '2 cups panko bread crumbs',
                        '1 cup freshly grated Parmesan cheese',
                        '1/2 cup all-purpose flour',
                        '4 large eggs, beaten',
                        '1 1/2 cups marinara sauce',
                        '1 1/2 cups shredded mozzarella cheese',
                        '1/4 cup chopped fresh basil leaves',
                        '2 tablespoons chopped fresh parsley leaves',
                        '2 tablespoons unsalted butter, cut into small pieces'],
        'servings': 4,
        'instruction': ['1. Preheat the oven to 400°F (200°C).',
                        '2. In a shallow bowl, mix together the breadcrumbs and grated parmesan cheese.',
                        '3. In another shallow bowl, place the flour.',
                        '4. In a third shallow bowl, beat the eggs.',
                        '5. Season the chicken breasts with salt and pepper.',
                        '6. Dredge each chicken breast in the flour, shaking off any excess.',
                        '7. Dip each chicken breast in the beaten egg, then coat in the breadcrumb mixture, pressing the breadcrumbs onto the chicken to adhere.',
                        '8. Place the chicken breasts on a baking sheet sprayed with olive oil cooking spray.',
                        '9. Bake the chicken for 20-25 minutes or until cooked through and golden brown.',
                        '10. Remove the chicken from the oven and spoon marinara sauce over each chicken breast.',
                        '11. Sprinkle shredded mozzarella cheese over the top of each chicken breast.',
                        '12. Return the chicken to the oven and bake for an additional 10-15 minutes or until the cheese is melted and bubbly.',
                        '13. Remove the chicken from the oven and let it rest for 5 minutes before serving.',
                        '14. Garnish the chicken with chopped fresh basil before serving.'],
        'description': 'Baked Chicken Parmesan is a classic Italian dish that is both hearty and satisfying. This easy recipe features crispy baked chicken topped with marinara sauce, melted mozzarella cheese, and fresh herbs. Serve it over spaghetti or with a side of garlic bread for a delicious meal that the whole family will love!',
        'tags': 'Regular',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': 'Crustless Caprese Quiche',
        'cook_time_str': '40 min',
        'prep_time_str': '10 min',
        'ingredients': ['Nonstick cooking spray',
                        '1/3 cup plus 2 tablespoons whole wheat', 
                        '2 teaspoons extra-virgin olive oil', 
                        '1 medium onion', 'Kosher salt', 
                        '4 plum tomatoes', 
                        '2 large eggs plus 2 large egg whites', 
                        '1/2 cup part-skim ricotta cheese', 
                        '1/2 cup 2-percent milk', 
                        '1/4 cup packed fresh basil leaves', 
                        '4 ounces shredded part-skim mozzarella'],
        'servings': 5,
        'instruction': ['1. Preheat the oven to 375°F (190°C).',
                        '2. Spray a 9-inch pie dish with cooking spray.',
                        '3. Scatter the cherry tomatoes, basil, and mozzarella cheese evenly in the pie dish.',
                        '4. In a large bowl, whisk together the eggs, heavy cream, salt, and pepper until well combined.',
                        '5. Pour the egg mixture over the tomato, basil, and cheese mixture.',
                        '6. Bake for 35-40 minutes or until the top is golden brown and the quiche is set in the center.',
                        '7. Let the quiche cool for a few minutes before slicing and serving.'],
        'description': 'A delicious and healthy breakfast or brunch dish that combines the flavors of a classic Caprese salad with the texture of a quiche. This recipe typically includes eggs, milk, fresh basil, tomatoes, and mozzarella cheese, all baked together in a pie dish or quiche pan. Without the crust, this quiche is lower in calories and gluten-free, making it a great option for those with dietary restrictions. It can be served warm or cold, and is perfect for a quick and easy meal any time of day.',
        'tags': 'Vegetarian',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': 'BBQ Spaghetti Squash Sliders',
        'cook_time_str': '1.5 hours',
        'prep_time_str': '20 min',
        'ingredients': ['1 spaghetti squash,',
                        'Kosher salt',
                        '¾ cup of bbq sauce',
                        '3 tablespoons pure maple syrup',
                        '2 tablespoons of tomato paste',
                        '⅔ cups plus 2 tablespoons apple cider vinegar',
                        '2 tablespoon mayonnaise',
                        '¼ small head red cabbage',
                        '¼ small red onion',
                        '24 mini slider buns',
                        '1 English cucumber'],
        'servings': 12,
        'instruction': ['1. Preheat oven to 350 degrees F, line a baking sheet with foil',
                        '2. Halve the squash lengthwise and scoop out the seeds. Season the flesh generously with salt and brush with 1/4 cup of the barbecue sauce. Arrange flesh-side down on the prepared baking sheet and roast until tender and the squash strands are easily separated with a fork, 45 minutes to 1 hour. Let cool for a few minutes on the baking sheet.',
                        '3. Meanwhile, whisk together the maple syrup, tomato paste, 2/3 cup of the vinegar, remaining 1/2 cup barbecue sauce, a pinch of salt and 1 cup water in a small saucepan. Bring to a boil, then reduce to a simmer and cook until thickened, 15 to 20 minutes. Keep warm.',
                        '4. Mix together the mayonnaise, cabbage, onion and remaining 2 tablespoons vinegar in a medium bowl—season with salt.',
                        '5. Use a fork to separate the squash strands (keep them in the skins). Divide 1 1/4 cups of the sauce between the 2 halves and mix until the squash strands are coated. Season with salt.',
                        '6. Slice the buns open about three-quarters of the way. Divide the cucumber slices among the buns. Fill each with a generous amount of the squash and top with some slaw. Serve with extra sauce on the side.'],
        'description': 'A delicious vegetarian alternative to pulled pork sliders. The dish consists of roasted spaghetti squash, mixed with a homemade BBQ sauce, served on mini slider buns with a crunchy slaw made from red cabbage and red onion. The sliders are topped with fresh cucumber slices and extra BBQ sauce on the side. The combination of savory BBQ sauce and the sweetness of the roasted spaghetti squash make these sliders a tasty and healthy option for a meal or appetizer.',
        'tags': 'Vegetarian',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': 'Chipotle-Inspired Vegetarian Burrito Bowl',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    },
    {
        'recipe_name': '',
        'cook_time_str': '',
        'prep_time_str': '',
        'ingredients': [''],
        'servings': 1,
        'instruction': [''],
        'description': '',
        'tags': '',
        'likes': 0,
        'comments': ''
    }
]

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS recipes''')

cursor.execute('''CREATE TABLE recipes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  servings INTEGER,
                  prep_time INTEGER,
                  cook_time INTEGER,
                  description TEXT,
                  ingredients TEXT,
                  instructions TEXT)''')

for recipe in recipes:
    prep_time = time_to_minutes(recipe['prep_time_str'])
    cook_time = time_to_minutes(recipe['cook_time_str'])

    if 'instructions' in recipe:
        instructions = recipe['instructions']
    else:
        instructions = ''

    cursor.execute('''INSERT INTO recipes(title, servings, prep_time, cook_time, description, ingredients, instructions)
                      VALUES(?,?,?,?,?,?,?)''',
                   (recipe['recipe_name'], recipe['servings'], prep_time, cook_time, recipe['description'], ', '.join(recipe['ingredients']), instructions))

conn.commit()

# retrieve all rows from the "recipes" table
cursor.execute('''SELECT * FROM recipes''')
rows = cursor.fetchall()

# print each row
for row in rows:
    print(row)

conn.close()
