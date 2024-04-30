import concurrent.futures  
import time      
from datetime import date         
import requests      

# Gourmai #
from gourmai.meal.recipe_generation import *
from gourmai.meal.get_functions.utils import *

from gourmai.meal.get_functions.get_name import get_name
from gourmai.meal.get_functions.get_beverage import get_beverage
from gourmai.meal.get_functions.get_equipment import get_equipment
from gourmai.meal.get_functions.get_history import get_history
from gourmai.meal.get_functions.get_image import get_image
from gourmai.meal.get_functions.get_ingredients import get_ingredients, get_altered_ingredients
from gourmai.meal.get_functions.get_method import get_method
from gourmai.meal.get_functions.get_nutrition import get_nutrition
from gourmai.meal.get_functions.get_origin import get_origin
from gourmai.meal.get_functions.get_summary import *
from gourmai.meal.get_functions.get_tags import get_tags
from gourmai.meal.get_functions.get_time import get_time
from gourmai.meal.get_functions.get_cuisine import get_cuisine

from gourmai.meal.models import *

def append_ingredients_to_recipe(ingredients_json, recipe):
    for ingredient_name, quantity in ingredients_json.items():
        # Check if the ingredient already exists in the database
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        
        if not ingredient:
            # If the ingredient doesn't exist, create a new ingredient instance
            ingredient = Ingredient(name=ingredient_name)
            db.session.add(ingredient)
        
        # Create a new RecipeIngredient instance and link it to the recipe and ingredient
        recipe_ingredient = RecipeIngredient(quantity=quantity, recipe=recipe, ingredient=ingredient)
        
        # Add the RecipeIngredient object to the session
        db.session.add(recipe_ingredient)
    
    # Commit changes to the database
    db.session.commit()


def append_beverage_to_recipe(beverage_json, recipe):
    for beverage_name, beverage_description in beverage_json.items():
        beverage_obj = BeveragePairing(
            beverage_name=beverage_name,
            beverage_description=beverage_description,
            recipe=recipe
        )
        db.session.add(beverage_obj)
    db.session.commit()

def append_nutrition_to_recipe(nutrition_json, recipe):
    nutrition_obj = Nutrition(
        calories=nutrition_json.get("calories", 0),
        carbohydrates=nutrition_json.get("carbohydrates", 0),
        cholesterol=nutrition_json.get("cholesterol", 0),
        total_fat=nutrition_json.get("total_fat", 0),
        saturated_fat=nutrition_json.get("saturated_fat", 0),
        trans_fat=nutrition_json.get("trans_fat", 0),
        fibre=nutrition_json.get("fibre", 0),
        protein=nutrition_json.get("protein", 0),
        sodium=nutrition_json.get("sodium", 0),
        sugar=nutrition_json.get("sugar", 0),
        potassium=nutrition_json.get("potassium", 0),
        recipe=recipe
    )

    db.session.add(nutrition_obj),
    db.session.commit()

def append_image_to_recipe(image_data, recipe):
    image_obj = Images(
        image=image_data,
        recipe=recipe
    )

    db.session.add(image_obj),
    db.session.commit()

# Threaded get_recipe #
def get_recipe(user_input):

    #### This is the main funciton called when generating a recipe. ###
    #### It incorperates all above functions into one function to be called from the views.py ### 
    #### After getting all of the results it puts them into a class and returns it ### 
    print("get_recipe() started...")

    # Record the time #
    start_time = time.time()

    # This is the multithreading call #
    # This will run multiple functions simultaniously in "threads" # 
    with concurrent.futures.ThreadPoolExecutor() as executor:


        # Thread 1: Get Name # 
        recipe_name_future = executor.submit(get_name, user_input)


        # Await recipe name response #
        recipe_name = recipe_name_future.result()


        # Thread 2: Dependent on Name #
        ingredients_future = executor.submit(get_ingredients, recipe_name, user_input) # returns json string #
        origin_future = executor.submit(get_origin, recipe_name)
        history_future = executor.submit(get_history, recipe_name)
        cuisine_future = executor.submit(get_cuisine, recipe_name)
        

        # Await ingredient response #
        ingredients = ingredients_future.result()


        # Thread 3: Dependent on Ingredients # 
        tags_future = executor.submit(get_tags, ingredients)
        image_future = executor.submit(get_image, recipe_name, ingredients)
        beverage_future = executor.submit(get_beverage, recipe_name, ingredients)
        method_future = executor.submit(get_method, recipe_name, ingredients, user_input)
        nutrition_future = executor.submit(get_nutrition, ingredients, recipe_name)


        # Await method response #
        method = method_future.result()


        # Thread 4: Dependent on Method
        equipment_future = executor.submit(get_equipment, method)
        time_future = executor.submit(get_time, method)
        summary_future = executor.submit(get_summary, recipe_name, method)


        # Await other responses. # 
        nutrition = nutrition_future.result()
        equipment = equipment_future.result()
        prep_time, cook_time, total_time = time_future.result()
        allergen_tags, diet_tags = tags_future.result()
        image = image_future.result()
        beverage_json = beverage_future.result()
        current_date = date.today()

        # When ready create the recipe object. # 
        recipe = Recipes(
            recipe_name=recipe_name, # String # 
            summary=summary_future.result(), # String # 
            history=history_future.result(), # String # 
            origin=origin_future.result(), # String #   
            equipment=equipment, # list of strings #
            method=method, # list of strings #            
            prep_time=prep_time, # int #
            cook_time=cook_time, # int #
            total_time=total_time, # int #
            allergen_tags=allergen_tags, # list of strings #
            diet_tags=diet_tags, # list of strings #
            cuisine=cuisine_future.result(), # string #
            servings=user_input['servings'], # string #
            difficulty=user_input['difficulty'], # string #
            date_created=current_date,
        )
        
        db.session.add(recipe)
        db.session.flush()
        
        recipe_id = recipe.id

        # Append sub tables to recipe #
        append_nutrition_to_recipe(nutrition, recipe)
        append_ingredients_to_recipe(ingredients, recipe)
        append_image_to_recipe(image, recipe)
        
        append_beverage_to_recipe(beverage_json, recipe)


        # Print recipe generation time #
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_elapsed_time = f"{elapsed_time:.3f}"
        print("Recipe generation sucessful")
        print(f"Recipe generation time: {formatted_elapsed_time} seconds")

    # Return recipe object. #
    return recipe