import os
import json

# Flask #
from flask import render_template, redirect, request, url_for, g, Response, session, current_app, send_from_directory, flash, app, jsonify
from flask_login import current_user, login_user, logout_user, LoginManager, login_required

# Gourmai #
from gourmai import db, login_manager
from gourmai.canvas import blueprint
from gourmai.auth.models import Users
from gourmai.canvas.forms import ContactUsForm

from gourmai.meal.models import Recipes


@blueprint.route('/settings')
def settings():
    return render_template('canvas/settings.html')


@blueprint.route('/terms')
def terms():
    return render_template('canvas/terms.html')


@blueprint.route('/contact')
def contact():
    contact_form = ContactUsForm() 
    return render_template('canvas/contact.html', form=contact_form)


@blueprint.route('/recipe_book', methods=['GET'])
@login_required
def recipe_book():

    # Check if the user is logged in #
    if current_user.is_authenticated:

        saved_recipes = current_user.recipes

        for recipe in saved_recipes:
            # Check if recipe from DB needs to be loaded into JSON #
            recipe_attributes = vars(recipe)
            for key, value in recipe_attributes.items():
                if isinstance(value, str):
                    try:
                        setattr(recipe, key, json.loads(value))
                    except json.JSONDecodeError as e:
                        pass # If it errors no need for a json.loads # 

        return render_template(
            'canvas/recipe_book.html',
            saved_recipes=saved_recipes
            )
    
    # Redirect to login page #
    else:
        # Initialize the login form
        login_form = LoginForm()

        return render_template(
            'auth/login.html',
            error='Please log in to save recipe!',
            form=login_form
            )


@blueprint.route('/api/get_saved_recipe/<user_id>', methods=['GET'])
def api_get_saved_recipe(user_id):

    # Get data
    user = Users.query.filter_by(id=user_id).first()
    recipes = user.recipes

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

