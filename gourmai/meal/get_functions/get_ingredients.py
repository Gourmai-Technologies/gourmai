import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *
# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_ingredients(recipe_name, user_input):
    
    servings = user_input['servings']
    difficulty = user_input['difficulty']
    dietary_restriction = user_input['dietaryRestrictions']
    time_input = user_input['time']
    unit = user_input['unit']

    input_context = "We're aiming to build an extensive digital cookbook for food enthusiasts."

    

    instruction = (
        f"You must give the ingredients that would be used to create the recipe '{recipe_name}' that serves exactly one person. Make sure this is a comprehensive and complete list exactly for the recipe specified. The cooking skill level is '{difficulty}'.\n"
        f"Please provide all units in '{unit}'."
        f"The user has the dietary restriction '{dietary_restriction}', please adhere to the ingredients to this at all costs.\n"
        f"Question: Please provide a list of ingredients for making the recipe {recipe_name}.\n"
        f"Ensure the output is in the format of a dictionary where each key is an ingredient and its value is the quantity.\n"
        f"Do not include the name of the recipe in the output.\n"
        f"More experienced users want to make their own food, things like pizza dough should be homemade.\n"
    )
    output_format = "output will always be given in a json object format!"
    specific_output_format = "{{ingredient : quantity}}, {{ingredient : quantity}},{{ingredient : quantity}}, {{ingredient : quantity}},"

    example_json = (
        "{'Red wine': '150', "
        "'Chicken thigh': '1', "
        "'Bacon': '2 slices', "
        "'Onion': '1', "
        "'Carrot': '1', "
        "'Garlic': '2 cloves', "
        "'Bay leaf': '1', "
        "'Thyme': '1 sprig', "
        "'Flour': '1', "
        "'Chicken stock': '100', "
        "'Butter': '1', "
        "'Salt and pepper': 'To taste'}"
    )

    # Full string given to the AI #
    prompt = (
        f"Input context: {input_context},\n"
        f"Instruction: {instruction},\n"
        
        f"Output Format: {specific_output_format},\n"
        f"Example JSON: {example_json},\n"
    )

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a culinary expert ingredient lists for recipes based on a set of perameters."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

    
def get_altered_ingredients(recipe_name, new_ingredients):
        
    instruction = (
        "You will provided with a user updated set of ingredients. Your job is to provide appropriate quantities for each ingredient based on a recipe name you will also be provided with."
    )
    output_format = "json object"
    specific_output_format = "{{ingredient : quantity}}, {{ingredient : quantity}},{{ingredient : quantity}}, {{ingredient : quantity}},"

    example_json = (
        "{'Red wine': '150', "
        "'Chicken thigh': '1', "
        "'Bacon': '2 slices', "
        "'Onion': '1', "
        "'Carrot': '1', "
        "'Garlic': '2 cloves', "
        "'Bay leaf': '1', "
        "'Thyme': '1 sprig', "
        "'Flour': '1', "
        "'Chicken stock': '100', "
        "'Butter': '1', "
        "'Salt and pepper': 'To taste'}"
    )

    # Full string given to the AI #
    prompt = (
        f"Output format: {output_format}"
        f"Output Example: {specific_output_format}"
        f"Instruction: {instruction}"
        f"New ingredient list: {new_ingredients}"
        f"Recipe name {recipe_name}"
        f"Please return ingredients and quantities for the recipe {recipe_name}"
    )

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a culinary expert ingredient lists for recipes based on a set of perameters."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return JSON # 
    return json.loads(response.choices[0].message.content)