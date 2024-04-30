# Flask #
from flask import render_template, redirect, request, url_for, g, Response, session, current_app, send_from_directory, flash, app, jsonify
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
import base64
# Gourmai #
from gourmai import db, login_manager
from gourmai.discovery import blueprint
from gourmai.meal.models import Recipes, RecipeIngredient, Ingredient

# sqlalchemy #
from sqlalchemy import or_, and_, cast, ARRAY, any_
from sqlalchemy.dialects import postgresql


@blueprint.route('/')
def load_discovery():
    dietary_restrictions = request.args.get('diet-filters-input') # comma seperated string
    allergens = request.args.get('allergen-filters-input')
    search_query = request.args.get('search-query')
    ingredient_search_query = request.args.get('ingredient-query')
    cuisine_search_query = request.args.get('cuisine-query')

    # Start with an unfiltered query #
    recipes_query = Recipes.query

    if search_query:
        search_query = search_query.strip()  # Remove leading/trailing whitespaces
        recipes_query = recipes_query.filter(Recipes.recipe_name.ilike(f'%{search_query}%'))

    if ingredient_search_query:
        ingredient_search_query = ingredient_search_query.strip()
        recipes_query = recipes_query.filter(
            Recipes.id.in_(
                db.session.query(RecipeIngredient.recipe_id)
                .join(Ingredient)
                .filter(Ingredient.name.ilike(f'%{ingredient_search_query}%'))
            )
        )

    if cuisine_search_query:
        cuisine_search_query = cuisine_search_query.strip()
        recipes_query = recipes_query.filter(Recipes.cuisine.ilike(f'%{cuisine_search_query}%'))

 
    # Apply filters based on the diet tags if restrictions are provided
    if dietary_restrictions:
        print("Applying filters based on restrictions:", dietary_restrictions)
        dietary_restrictions_list = dietary_restrictions.split(',')  # Split the restrictions string into a list
        recipes_query = recipes_query.filter(Recipes.diet_tags.cast(ARRAY(db.String)).op('@>')(dietary_restrictions_list))

    if allergens:
        print("Filtering based on allergens:", allergens)
        allergen_list = allergens.split(',')  # Split the allergens string into a list
        for allergen in allergen_list:
            recipes_query = recipes_query.filter(~Recipes.allergen_tags.cast(ARRAY(db.String)).any(allergen))

    # Execute the query and limit the number of results
    recipes = recipes_query.order_by(Recipes.id.desc()).limit(12).all()

    return render_template('discovery/discovery.html', recipes=recipes)
 

@blueprint.route('/api/load')
def load_discovery_api():

    # Execute the query and limit the number of results
    recipes = Recipes.query.order_by(Recipes.id.desc()).limit(8).all()

    # Convert query result to JSON 
    recipes_json = []
    for recipe in recipes:
        recipe_images = []

        for image_obj in recipe.images:
            # Assuming image_obj.image_data contains the byte-like object representing the image data
            image_data = image_obj.image

            # Convert the byte-like object to base64 string for JSON serialization
            
            recipe_images.append({'image': image_data})

        recipe_id = recipe.id  

        # Add the recipe details along with the decoded image data to the JSON object
        recipes_json.append({
            'recipe_name': recipe.recipe_name,
            'recipe_id' : recipe_id,
            'recipe_images': recipe_images[0]
        })

    return jsonify(recipes=recipes_json)

@blueprint.route('/filter')
def filter():
    dietary_restrictions = request.args.get('diet-filters-input')
    allergens = request.args.get('allergen-filters-input')
    search_query = request.args.get('search-query')
    ingredient_search_query = request.args.get('ingredient-query')
    cuisine_search_query = request.args.get('cuisine-query')

    recipes_query = Recipes.query

    if search_query:
        search_query = search_query.strip()
        recipes_query = recipes_query.filter(Recipes.recipe_name.ilike(f'%{search_query}%'))

    if ingredient_search_query:
        ingredient_search_query = ingredient_search_query.strip()
        recipes_query = recipes_query.filter(
            Recipes.id.in_(
                db.session.query(RecipeIngredient.recipe_id)
                .join(Ingredient)
                .filter(Ingredient.name.ilike(f'%{ingredient_search_query}%'))
            )
        )

    if cuisine_search_query:
        cuisine_search_query = cuisine_search_query.strip()
        recipes_query = recipes_query.filter(Recipes.cuisine.ilike(f'%{cuisine_search_query}%'))

    if dietary_restrictions:
        dietary_restrictions_list = dietary_restrictions.split(',')
        recipes_query = recipes_query.filter(Recipes.diet_tags.cast(ARRAY(db.String)).op('@>')(dietary_restrictions_list))

    if allergens:
        allergen_list = allergens.split(',')
        for allergen in allergen_list:
            recipes_query = recipes_query.filter(~Recipes.allergen_tags.cast(ARRAY(db.String)).any(allergen))

    recipes = recipes_query.order_by(Recipes.id.desc()).limit(12).all()
    # If there are no more recipes to load, return a response indicating so
    if not recipes:
        return jsonify(recipes=[], has_more=False)

    # Convert the recipes to a JSON format and return
    recipes_data = [
        {
            'recipe_name': recipe.recipe_name,
            'image': recipe.images[0].image if recipe.images else None,
            'id': recipe.id
        }
        for recipe in recipes
    ]
    return jsonify(recipes=recipes_data, has_more=True)


@blueprint.route('/load-more-recipes', methods=['GET'])
def load_more_recipes():
    print("loading more recipes")
    page = int(request.args.get('page', 1))  # Get the current page number
    batch_size = int(request.args.get('batch_size', 12))  # Get the batch size
    dietary_restrictions = request.args.get('diet-filters-input')  # comma-separated string
    allergens = request.args.get('allergen-filters-input')
    search_query = request.args.get('search-query')
    ingredient_search_query = request.args.get('ingredient-query')
    cuisine_search_query = request.args.get('cuisine-query')

    # Start with an unfiltered query
    recipes_query = Recipes.query

    if search_query:
        search_query = search_query.strip()  # Remove leading/trailing whitespaces
        recipes_query = recipes_query.filter(Recipes.recipe_name.ilike(f'%{search_query}%'))

    if ingredient_search_query:
        ingredient_search_query = ingredient_search_query.strip()
        recipes_query = recipes_query.filter(
            Recipes.id.in_(
                db.session.query(RecipeIngredient.recipe_id)
                .join(Ingredient)
                .filter(Ingredient.name.ilike(f'%{ingredient_search_query}%'))
            )
        )

    if cuisine_search_query:
        cuisine_search_query = cuisine_search_query.strip()
        recipes_query = recipes_query.filter(Recipes.cuisine.ilike(f'%{cuisine_search_query}%'))

    # Apply filters based on the diet tags if restrictions are provided
    if dietary_restrictions:
        print("Applying filters based on restrictions:", dietary_restrictions)
        dietary_restrictions_list = dietary_restrictions.split(',')  # Split the restrictions string into a list
        recipes_query = recipes_query.filter(Recipes.diet_tags.cast(ARRAY(db.String)).op('@>')(dietary_restrictions_list))

    if allergens:
        print("Filtering based on allergens:", allergens)
        allergen_list = allergens.split(',')  # Split the allergens string into a list
        for allergen in allergen_list:
            recipes_query = recipes_query.filter(~Recipes.allergen_tags.cast(ARRAY(db.String)).any(allergen))

    # Calculate the offset based on the current page number and batch size
    offset = (page) * batch_size

    # Query the database to fetch the next batch of recipes
    recipes = recipes_query.order_by(Recipes.id.desc()).offset(offset).limit(batch_size).all()

    # If there are no more recipes to load, return a response indicating so
    if not recipes:
        return jsonify(recipes=[], has_more=False)

    # Convert the recipes to a JSON format and return
    recipes_data = [
        {
            'recipe_name': recipe.recipe_name,
            'image': recipe.images[0].image if recipe.images else None,
            'id': recipe.id
        }
        for recipe in recipes
    ]
    return jsonify(recipes=recipes_data, has_more=True)




@blueprint.route('/api/load-more-recipes/<page_number>', methods=['GET'])
def api_load_more_recipes(page_number):

    print(page_number)
    batch_size = 8
    offset = int(page_number) * batch_size

    # Query the database to fetch the next batch of recipes
    recipes = Recipes.query.order_by(Recipes.id.desc()).offset(offset).limit(batch_size).all()
    
    # Convert query result to JSON 
    recipes_json = []
    for recipe in recipes:
        recipe_images = []

        for image_obj in recipe.images:
            # Assuming image_obj.image_data contains the byte-like object representing the image data
            image_data = image_obj.image

            # Convert the byte-like object to base64 string for JSON serialization
            
            recipe_images.append({'image': image_data})

        recipe_id = recipe.id  

        # Add the recipe details along with the decoded image data to the JSON object
        recipes_json.append({
            'recipe_name': recipe.recipe_name,
            'recipe_id' : recipe_id,
            'recipe_images': recipe_images[0]
        })


    return jsonify(recipes=recipes_json)
