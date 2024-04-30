import json
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Flask #
from flask_login import current_user, login_required
from flask import request, render_template, g, app, session, jsonify, abort, redirect, url_for

# Gourmai #
from gourmai.auth.models import Users, user_recipe_association
from gourmai.meal.models import Recipes, Suggestions
from gourmai.meal import blueprint
from gourmai.meal.recipe_generation import get_main_course_suggestion, get_side_suggestion

from gourmai.meal.get_functions.get_summary import get_concise_summary
from gourmai.meal.get_functions.get_question_answer import get_question_answer
from gourmai.meal.get_recipe import get_recipe
from gourmai.meal.get_altered_recipe import get_altered_recipe
from gourmai.meal.get_functions.get_alternative_ingredients import *
from gourmai import db
from gourmai.home.utils import *

from sqlalchemy import delete

from sqlalchemy.orm import sessionmaker

# Forms #
from gourmai.canvas.forms import ContactUsForm
from gourmai.auth.forms import LoginForm

# Init #
load_dotenv()

# This is the route that generates the recipe given a user input. #
@blueprint.route('/generate-recipe', methods=['POST'])
def generate_recipe():

    # Check if the user is logged in # 
    # If so get their dietary restriction details #
    if current_user.is_authenticated:
        dietary_restrictions = current_user.dietary_restrictions
        if dietary_restrictions == {}:
            dietary_restrictions = None
    else: dietary_restrictions = None

    # Get user input from form. #
    user_input = {
        'recipe_input': request.form.get('recipeInput', ''),
        'ingredientSuggestion': request.form.get('ingredientSuggestion', ''),
        'contextSuggestion': request.form.get('contextSuggestion', ''),
        'difficulty': request.form.get('difficultyValue', 'Intermediate'),
        'cuisine': request.form.get('cuisine', ''),
        'diet': request.form.get('diet', ''),
        'servings' : request.form.get('servings') or '1',
        'time' : request.form.get('timeValue', '30 - 45 mins'),
        'dietaryRestrictions' : dietary_restrictions,
        'unit' : request.form.get('unitInput', 'metric')
    }

    # Store the input in cache #
    session['user_input'] = user_input

    # Generate recipe object. #
    try:
        new_recipe = get_recipe(user_input)
    
    # If fail, send user to home page. Display error. #
    except Exception as e:
        raise e
        return render_template(
            'home/index.html',
            recipe_failed_error_message="Recipe Generation Failed. Please try again."
        )
    
    # Save recipe to database. #
    try:
        db.session.add(new_recipe)
        db.session.commit()

        # Store recipe ID in cache #
        session['current_recipe_id'] = new_recipe.id

    except Exception as e:
        print(f"An error occured while storing the recipe to the DB: {e}")


    # Send user to the "load_recipe()" route along with recipe ID. #
    return redirect(url_for('meal_bp.load_recipe', recipe_id=new_recipe.id))


# This route changes an existing recipe. #
# The recipe object and the users' changes are passed. #
@blueprint.route('/generate-altered-recipe', methods=['POST'])
def generate_altered_recipe():

    # Get JSON data from client #
    data = request.get_json()

    if data:
        # Extract data from JSON #
        recipe_id = data.get('recipeID')
        altered_ingredients = data.get('ingredients')
        user_input = session.get('user_input')

        # Get original recipe object #
        original_recipe = Recipes.query.get(recipe_id)
        
        # Return new recipe # This function is simalar to the get_recipe function with some minor changes. #
        altered_recipe = get_altered_recipe(original_recipe, altered_ingredients)
        
        # Add recipe to db. #
        db.session.add(altered_recipe)
        db.session.commit()

        # Store ID in cache #
        session['current_recipe_id'] = altered_recipe.id

        # Return the altered recipe ID as JSON response
        return jsonify({'recipe_id': altered_recipe.id})
    
    # Return an error response if data is missing
    return jsonify({'error': 'Invalid request data'}), 400 


# Currently not in use. # 
# This was the list of recipe names and discriptions #
@blueprint.route('/generate-recipe-from-suggestions', methods=['POST'])
def generate_recipe_from_suggestions():

    if str(request.form.get('selectedSideSuggestion')) != "":
        # Get the user input data from form on index. #
        recipe_input = str(session.get('main_selection')) + " with a side of " + str(request.form.get('selectedSideSuggestion'))
    else: 
        recipe_input = str(session.get('main_selection'))

    if current_user.is_authenticated:
        dietary_restrictions = current_user.dietary_restrictions
        if dietary_restrictions == {}:
            dietary_restrictions = None
    else: dietary_restrictions = None

    user_input = {
        'recipe_input': recipe_input,
        'ingredientSuggestion': request.form.get('ingredientSuggestion', ''),
        'contextSuggestion': request.form.get('contextSuggestion', ''),
        'difficulty': request.form.get('difficultyValue', 'Intermediate'),
        'cuisine': request.form.get('cuisine', ''),
        'diet': request.form.get('diet', ''),
        'servings' : request.form.get('servings') or '1',
        'time' : request.form.get('timeValue', '30 - 45 mins'),
        'dietaryRestrictions' : dietary_restrictions,
        'unit' : request.form.get('unitInput', 'metric') 
    }

    # Save user input (from index form) in session #
    session['user_input'] = user_input

    ### Generate recipe object. ###
    try:
        
        recipe = get_recipe(user_input)
    except Exception as e:
        print(f"\n\nRecipe generation failed{e}\n\n")
        return render_template(
            'home/index.html',
            recipe_failed_error_message="Recipe Generation Failed. Please try again."
        )

    ### Save recipe to database ###
    try:
        db.session.add(recipe)
        db.session.commit()

        print(recipe.date_created)

        # Store ID in session #
        session['current_recipe_id'] = recipe.id

        # Return recipe from db #
        recipe = Recipes.get_recipe_by_id(db.session, recipe.id)

    except Exception as e:
        print(f"An error occured while storing the recipe to the DB:  {e}")

    # Check if recipe from DB needs to be loaded into JSON #
    recipe_attributes = vars(recipe)
    for key, value in recipe_attributes.items():
        if isinstance(value, str):
            try:
                setattr(recipe, key, json.loads(value))
            except json.JSONDecodeError as e:
                pass # If it errors no need for a json.loads # 

    try:
        # Inject dynamic variables to HTML using render_template() #     
        return redirect(url_for('meal_bp.load_recipe', recipe_id=recipe.id))

    except Exception as e:
        raise Exception(f"An error occured while injecting recipe data into HTML.: {e}")
        # Initialize the login form #


# When the user presses the "change" button. It returns a list of ingredients that the ingredient could be swapped with. # BROKEN #
@blueprint.route('/generate-ingredient-alternatives', methods=['POST'])
def generate_ingredient_alternatives():
    data = request.get_json()

    if data:
        recipe_name = data.get('recipeName')
        ingredient_name = data.get('ingredientName')
    
        alternatives = get_alternative_ingredients(recipe_name, ingredient_name)

        # Assuming alternatives is already in JSON format
        return alternatives, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'error': 'No data received'}), 400

# This is suplementary to the suggestion boxes. #
@blueprint.route('/regenerate-suggestions', methods=['POST'])
def regenerate_recipe_suggestion():
    
    user_input = session.get('user_input')
    suggestions = get_main_course_suggestion(user_input)

    mainsummary1 = get_concise_summary(suggestions['suggestion1'])
    mainsummary2 = get_concise_summary(suggestions['suggestion2'])
    mainsummary3 = get_concise_summary(suggestions['suggestion3'])
    mainsummary4 = get_concise_summary(suggestions['suggestion4'])
    mainsummary5 = get_concise_summary(suggestions['suggestion5'])

    # Pop existing session variables if they exist
    session.pop('suggestions', None)
    session.pop('mainsummary1', None)
    session.pop('mainsummary2', None)
    session.pop('mainsummary3', None)
    session.pop('mainsummary4', None)
    session.pop('mainsummary5', None)

    # Save in session for later #
    session['suggestions'] = suggestions
    session['mainsummary1'] = mainsummary1
    session['mainsummary2'] = mainsummary2
    session['mainsummary3'] = mainsummary3
    session['mainsummary4'] = mainsummary4
    session['mainsummary5'] = mainsummary5

    return render_template(
        'discovery/discovery.html',
        suggestion1=suggestions['suggestion1'],
        mainsummary1=mainsummary1,

        suggestion2=suggestions['suggestion2'],
        mainsummary2=mainsummary2,

        suggestion3=suggestions['suggestion3'],
        mainsummary3=mainsummary3,

        suggestion4=suggestions['suggestion4'],
        mainsummary4=mainsummary4,

        suggestion5=suggestions['suggestion5'],
        mainsummary5=mainsummary5
    )

#  This is suplementary to the suggestion boxes. #
@blueprint.route('/generate-sides', methods=['POST'])
def generate_sides():

    user_input = session.get('user_input')

    main_selection = request.form.get('selectedMainSuggestion')
    session['main_selection'] = main_selection

    print(main_selection)

    sides = get_side_suggestion(user_input, main_selection)

    # Get data from db #
    suggestions_id = session.get('current_suggestions_id')
    suggestions_data = Suggestions.get_row_by_id(db.session, suggestions_id)


    # Try to json.load each item #
    try:
        suggestions = json.loads(suggestions_data.suggestions)
    except TypeError:
        suggestions = suggestions_data.suggestions

    try:
        mainsummary1 = json.loads(suggestions_data.mainsummary1)
    except TypeError:
        mainsummary1 = suggestions_data.mainsummary1

    try:
        mainsummary2 = json.loads(suggestions_data.mainsummary2)
    except TypeError:
        mainsummary2 = suggestions_data.mainsummary2

    try:
        mainsummary3 = json.loads(suggestions_data.mainsummary3)
    except TypeError:
        mainsummary3 = suggestions_data.mainsummary3

    try:
        mainsummary4 = json.loads(suggestions_data.mainsummary4)
    except TypeError:
        mainsummary4 = suggestions_data.mainsummary4

    try:
        mainsummary5 = json.loads(suggestions_data.mainsummary5)
    except TypeError:
        mainsummary5 = suggestions_data.mainsummary5


    return render_template(
        'discovery/discovery.html',
        suggestion1=suggestions['suggestion1'],
        mainsummary1=mainsummary1,

        suggestion2=suggestions['suggestion2'],
        mainsummary2=mainsummary2,

        suggestion3=suggestions['suggestion3'],
        mainsummary3=mainsummary3,

        suggestion4=suggestions['suggestion4'],
        mainsummary4=mainsummary4,

        suggestion5=suggestions['suggestion5'],
        mainsummary5=mainsummary5,

        side1=sides['side1'],
        side2=sides['side2'],
        side3=sides['side3'],
        side4=sides['side4'],
        side5=sides['side5']
    )

# Returns question answer # BROKEN #




@blueprint.route('/ask-question', methods=['POST'])
def ask_question():
    
    user_input = session.get('user_input')
    current_recipe_id = session.get('current_recipe_id')

    form_data = request.form
    question = request.form.get('question')

    # Get current_recipe from DB #
    recipe = Recipes.get_recipe_by_id(db.session, current_recipe_id)

    question_answer = get_question_answer(question, recipe)
    response = jsonify({'message': question_answer})
    return response

# For dev #
@blueprint.route('/test-recipe', methods=['GET'])
def test_recipe():
    return redirect(url_for('meal_bp.load_recipe', recipe_id=400))
    

# Takes recipe ID and renders the page. #
@blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def load_recipe(recipe_id):

    # Get the ID from the http ^ #
    recipe = Recipes.query.get(recipe_id)
    session['current_recipe_id'] = recipe.id
    if recipe is None:
        abort(404)  # Recipe not found

    # Check if recipe from DB needs to be loaded into JSON # This is a stupid bit of code that checks each item in the object to see if it needs to be a "real" dictionary. #
    recipe_attributes = vars(recipe)
    for key, value in recipe_attributes.items():
        if isinstance(value, str):
            try:
                setattr(recipe, key, json.loads(value))
            except json.JSONDecodeError as e:
                pass  # If it errors no need for a json.loads

    # Initiates contact form object (flask WTForms library.)
    contact_form = ContactUsForm()

    # More stupid code that fixes a TypeError #
    time_string = str(recipe.date_created)

    # Inject dynamic variables to HTML using render_template()
    try:
        return render_template('canvas/recipe.html', recipe=recipe, time_string=time_string, form=contact_form) 
    except Exception as e:
        raise Exception(f"An error occurred while injecting recipe data into HTML: {e}")

# Adds recipe object to the user object. #
@blueprint.route('/save-recipe', methods=['POST'])
def save_recipe():
    print("Save recipe initiated")
    # Check if the user is logged in #
    if current_user.is_authenticated:
        current_recipe_id = session.get('current_recipe_id')

        # Check if the recipe ID is already in current_user.recipes #
        if any(recipe.id == current_recipe_id for recipe in current_user.recipes):
            return jsonify({'message': 'Recipe already saved'})

        # Return recipe from ID #
        recipe = Recipes.query.get(current_recipe_id)

        # Add to users recipes #
        current_user.recipes.append(recipe)
        db.session.commit()

        return jsonify({'message': 'Recipe saved successfully'})

    # Redirect to login page #
    else:
        # Initialize the login form #
        login_form = LoginForm()

        return render_template('auth/login.html', error='Please log in to save recipe!', form=login_form)

# Remove recipe from user object. #
@blueprint.route('/remove-recipe', methods=['POST'])
def remove_recipe():

    # Get recipe ID #
    recipe_id = int(request.form.get('remove_recipe_id'))
    
    # Check if the user is logged in
    if current_user.is_authenticated:
        
        # Query the recipe by its ID # 
        # in format # var = table_obj.query.filter_by(column_name=var).first-obj-found. Speeds up the request.
        recipe = Recipes.query.filter_by(id=recipe_id).first()
        
        if recipe:
            # Remove the recipe from the current user's recipes
            current_user.recipes.remove(recipe)

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'success': True})
        else:
            # Return an error response if the recipe doesn't exist
            return jsonify({'error': 'Recipe not found'}), 404
    else:
        # Return an error response if the user is not authenticated
        return jsonify({'error': 'User not authenticated'}), 401


# Adds a dietary restriction to the user obj. #
@blueprint.route('/add-dietary-restriction', methods=['POST'])
def add_dietary_restriction():
    
    if current_user.is_authenticated:
        restriction = request.form.get('restriction')
        Users.add_dietary_restriction(current_user.id, restriction)
        return jsonify({'success': True})
    else:
        # Return an error response if the user is not authenticated
        return jsonify({'error': 'User not authenticated'}), 401


@blueprint.route('/remove-dietary-restriction', methods=['POST'])
def remove_dietary_restriction():

    if current_user.is_authenticated:
        item_to_remove = request.form.get('item')
        Users.remove_dietary_restriction(current_user.id, item_to_remove)

        return jsonify({'success': True})
    else:
        # Return an error response if the user is not authenticated
        return jsonify({'error': 'User not authenticated'}), 401


@blueprint.route('/update-measurement-units', methods=['POST'])
def change_user_measurement_units():

    if current_user.is_authenticated:
        measurement_unit = request.form.get('unit')
        print(measurement_unit)
        Users.update_measurement_units(measurement_unit)

        return jsonify({'success': True})
    else:
        # Return an error response if the user is not authenticated
        return jsonify({'error': 'User not authenticated'}), 401


##########################################################################################
# API #
##########################################################################################



# Restful recipe endpoint #
@blueprint.route('/api/recipe', methods=['GET', 'PUT', 'DELETE'])
def api_recipe():
    
    # Read # 
    if request.method == 'GET':

        # Get DB session #
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        # Get ID from client #
        recipe_id = request.args.get("recipeId")
                
        # Query db #
        recipe = Recipes.get_recipe_by_id(session, recipe_id)
        if recipe is None:
            abort(404)  # Recipe not found

        # Unpack the Image string from OBJ #
        recipe_images = []
        for image_obj in recipe.images:
            image_data = image_obj.image
            recipe_images.append({'image': image_data})
            
        # Unpack ingredients from obj #
        ingredient_list = []
        for recipe_ingredient in recipe.ingredients:
            ingredient_list.append({
                recipe_ingredient.ingredient.name : recipe_ingredient.quantity
            })
            
        # Serialize recipe object to JSON
        recipe = {
            'id': recipe.id,
            'recipe_name': recipe.recipe_name,
            'method': recipe.method,
            'summary': recipe.summary,
            'prep_time': recipe.prep_time,
            'cook_time': recipe.cook_time,
            'total_time': recipe.total_time,
            'servings': recipe.servings,
            'history': recipe.history,
            'origin': recipe.origin,
            'cuisine': recipe.cuisine,
            'difficulty': recipe.difficulty,
            'diet_conclusion': recipe.diet_conclusion,
            'equipment': recipe.equipment,
            'allergen_tags': recipe.allergen_tags,
            'diet_tags': recipe.diet_tags,
            'date_created': str(recipe.date_created),
            'ingredients': ingredient_list,
            'recipe_image': recipe_images[0]['image'],
            'nutrition': {
                'calories': recipe.nutrition.calories,
                'carbohydrates': recipe.nutrition.carbohydrates,
                'cholesterol': recipe.nutrition.cholesterol,
                'total_fat': recipe.nutrition.total_fat,
                'saturated_fat': recipe.nutrition.saturated_fat,
                'trans_fat': recipe.nutrition.trans_fat,
                'fibre': recipe.nutrition.fibre,
                'protein': recipe.nutrition.protein,
                'sodium': recipe.nutrition.sodium,
                'sugar': recipe.nutrition.sugar,
                'potassium': recipe.nutrition.potassium
            },
            'beverage_pairings': [{'name': pairing.beverage_name, 'description': pairing.beverage_description} for pairing in recipe.beverage_pairings]
        
        }

        return jsonify(recipe)

    # Update #
    elif request.method == 'PUT':
        return 404

    # Delete # 
    elif request.method == 'DELETE':
        return 404

@blueprint.route('/api/recipe/<user_id>', methods=['POST'])
def create_recipe(user_id):

    
    user = Users.query.filter_by(id=user_id).first()

    if user:
        dietary_restrictions = user.dietary_restrictions
        print(dietary_restrictions)
        if dietary_restrictions == {}:
            dietary_restrictions = None
    else:
        dietary_restrictions = None

    recipe_data = request.json

    user_input = {
        'recipe_input': recipe_data.get('name'),
        'ingredientSuggestion': recipe_data.get('ingredient-suggestion', ''),
        'contextSuggestion': recipe_data.get('context-suggestion', ''),
        'difficulty': recipe_data.get('difficulty', 'Intermediate'),
        'cuisine': recipe_data.get('cuisine', ''),
        'time': recipe_data.get('timeValue', '30 - 45 mins'),
        'dietaryRestrictions': dietary_restrictions,
        'unit': recipe_data.get('unitInput', 'metric'),
        'servings': recipe_data.get('servings') or '1',
    }

    new_recipe = get_recipe(user_input)

    db.session.add(new_recipe)
    db.session.commit()

    recipe_id = new_recipe.id

    return jsonify({'recipe_id': recipe_id})

# Restful Dietary Restriction Endpoint # 
@blueprint.route('/api/dietary-restrictions/<user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_dietary_restriction(user_id):

    # Get user #
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Read # 
    if request.method == 'GET':
        dietary_restrictions = json.loads(user.dietary_restrictions)
        return jsonify(dietary_restrictions)

    # Create #
    elif request.method == 'POST':
        restriction = request.json.get('restrictions')
        if not restriction:
            return jsonify({'error': 'Missing restriction data'}), 400
        user.dietary_restrictions.append(restriction)
        db.session.commit()
        return jsonify({'message': 'Dietary restriction added successfully'}), 201

    # Update #
    elif request.method == 'PUT':

        # Get the request JSON data #
        restriction_to_add = request.get_json().get('restriction')
        print(restriction_to_add)
        print(user.dietary_restrictions)

        if not restriction_to_add:
            return jsonify({'error': 'Missing restrictions data'}), 400

        # Convert from string to list , append, convert to string, save #
        restriction_list = json.loads(user.dietary_restrictions)
        restriction_list.append(restriction_to_add)
        restriction_string = json.dumps(restriction_list)
    
        user.dietary_restrictions = restriction_string
        db.session.commit()

        print(user.dietary_restrictions)
        
        return jsonify({'message': 'Dietary restrictions updated successfully'}), 200

    # Delete # 

    elif request.method == 'DELETE':

        # Get the request JSON data
        restriction_to_remove = request.form.get('restriction')

        # Get the list from DB
        restriction_list = json.loads(user.dietary_restrictions)

        # Initialize restriction_found
        restriction_found = False

        # Check if input is in array
        for item in restriction_list:
            if item == restriction_to_remove:
                restriction_list.remove(item)
                restriction_found = True
                break

        if restriction_found:
            restriction_string = json.dumps(restriction_list)
            user.dietary_restrictions = restriction_string  # Corrected attribute name
            db.session.commit()
            return jsonify({'message': f'{restriction_to_remove} deleted successfully.'}), 204
        else:
            return jsonify({'message': f'{restriction_to_remove} not found.'}), 404


# Restful Allergen Endpoint #
@blueprint.route('/api/allergens/<user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_allergen(user_id):

    # Get user #
    user = Users.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Read # 
    if request.method == 'GET':
        allergens_list = json.loads(user.allergens)
        return jsonify(allergen_list)

    # Create #
    elif request.method == 'POST':
        return jsonify({'error': 'Use PUT method to add allergen'}), 404

    # Update #
    elif request.method == 'PUT':

        # Get the request JSON data
        allergen = request.get_json().get('allergen')
        
        if not allergen:
            return jsonify({'error': 'Missing restrictions data'}), 400

        # Convert from string to list, append, convert to string, save #
        allergens_list = json.loads(user.allergens)
        allergens_list.append(allergen)
        allergens_string = json.dumps(allergens_list)

        user.allergens = allergens_string
        db.session.commit()

        print(user.allergens)

        return jsonify({'message': f'Added {allergen} to allergens successfully'}), 200

    # Delete # 
    elif request.method == 'DELETE':

        # Get the request JSON data
        allergen_to_remove = request.form.get('allergen')
        
        # Get the list from DB #
        allergens_list = json.loads(user.allergens)

        
        # Initialize allergen_found
        allergen_found = False

        # Check if input is in array #
        for item in allergens_list:
            if item == allergen_to_remove:
                allergens_list.remove(item)
                allergen_found = True
                break

        if allergen_found:
            allergens_string = json.dumps(allergens_list)
            user.allergens = allergens_string
            db.session.commit()
            return jsonify({'message': f'{allergen_to_remove} deleted successfully.'}), 204
        else:
            return jsonify({'message': f'{allergen_to_remove} not found.'}), 404


@blueprint.route('/api/user/recipes', methods=['GET'])
def get_user_recipes():
    user_id = request.args.get('user_id')
    
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 406

    recipes = user.recipes
    recipes_json = []
    for recipe in recipes:
        recipe_images = []

        for image_obj in recipe.images:
            image_data = image_obj.image
            recipe_images.append({'image': image_data})

        recipe_id = recipe.id  
        recipes_json.append({
            'recipe_name': recipe.recipe_name,
            'recipe_id' : recipe_id,
            'recipe_images': recipe_images[0]
        })

    return jsonify(recipes=recipes_json)

@blueprint.route('/api/user/recipes/<user_id>/<recipe_id>', methods=['PUT'])
def add_recipe_to_user(user_id, recipe_id):

    user = Users.query.filter_by(id=user_id).first()
    recipe = Recipes.query.filter_by(id=recipe_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 406
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 406

    # Check if the recipe is already saved for the user
    if recipe in user.recipes:
        return jsonify({'error': 'Recipe already saved for this user'}), 409

    user.recipes.append(recipe)
    db.session.commit()
    return jsonify({'success': True})

@blueprint.route('/api/user/recipes/<user_id>/<recipe_id>', methods=['DELETE'])
def remove_recipe_from_user(user_id, recipe_id):

    user = Users.query.filter_by(id=user_id).first()
    recipe = Recipes.query.filter_by(id=recipe_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 406
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 406

    
    user.recipes.remove(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe removed successfully'})

    # Query for all rows that match the user_id and recipe_id
    # Create a delete statement targeting the association table
    # delete_stmt = delete(user_recipe_association).where(user_recipe_association.c.user_id == user_id, user_recipe_association.c.recipe_id == recipe_id)

    # # Execute the delete statement
    # try:
    #     db.session.execute(delete_stmt)
    #     db.session.commit()
    #     return jsonify({'message': 'Deleted all associations successfully'}), 200
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({'error': str(e)}), 500

# Returns question answer to client # 
@blueprint.route('/api/ask-question/<recipe_id>/<question>', methods=['POST'])
def api_ask_question(recipe_id, question):

    # Get current_recipe from DB #
    recipe = Recipes.get_recipe_by_id(db.session, recipe_id)

    question_answer = get_question_answer(str(question), recipe)

    return question_answer



