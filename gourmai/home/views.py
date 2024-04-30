import json
from cryptography.fernet import Fernet

# Gourmai #
from gourmai.home import blueprint
from gourmai.auth.util import manage_cookie_policy
from gourmai.auth.forms import LoginForm
from gourmai.meal.models import Recipes
from gourmai.canvas.forms import ContactUsForm
from gourmai.home.utils import *

# Flask #
from flask import render_template, request, send_from_directory, current_app, session,jsonify
from flask_login import login_required, current_user

# Jinja #
from jinja2 import TemplateNotFound


# Index #
@blueprint.route('/home')
@manage_cookie_policy
def landing():
    return render_template('home/landing.html')

# Landing page # 
@blueprint.route('/')
@manage_cookie_policy
def index():
    return render_template('home/index.html')




@blueprint.route('/generate-link', methods=['POST'])
def generate_link():

    recipe_id = session['current_recipe_id']
    hashed_id = hash_id(recipe_id)
    return jsonify({'hashed_id': hashed_id})


@blueprint.route('/load-recipe/<hashed_recipe_id>', methods=['GET'])
def load_recipe_from_link(hashed_recipe_id):
    print(hashed_recipe_id)
    recipe_id = unhash_id(hashed_recipe_id)

    
    # Load recipe using the provided recipe_id
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        # Check if recipe from DB needs to be loaded into JSON
        recipe_attributes = vars(recipe)
        for key, value in recipe_attributes.items():
            if isinstance(value, str):
                try:
                    setattr(recipe, key, json.loads(value))
                except json.JSONDecodeError as e:
                    pass  # If it errors no need for a json.loads

        contact_form = ContactUsForm()

        # Inject dynamic variables to HTML using render_template()
        try:
            return render_template(
                'canvas/recipe.html',
                recipe=recipe,
                form=contact_form
            )
        except Exception as e:
            raise Exception(f"An error occurred while injecting recipe data into HTML.: {e}")
    else:
        return "Recipe not found", 404