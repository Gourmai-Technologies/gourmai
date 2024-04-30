import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *
from gourmai import db, session

# Flask 
from flask import current_app

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_name(user_input):

    
    name = user_input['recipe_input']
    servings = user_input['servings']
    ingredient_suggestion = user_input['ingredientSuggestion']
    context_suggestion = user_input['contextSuggestion']
    difficulty = user_input['difficulty']
    cuisine = user_input['cuisine']
    time_input = user_input['time']
    dietary_restrictions = user_input['dietaryRestrictions']
    

    response_style = "You are a chef tasked souly with supplying the names of good recipe names based on a set of perameters."
    
    instruction = (
    f"Generate a list of diverse and popular recipe names suitable for a cook at the '{difficulty}' difficulty level."
    "YOUR RECIPE SUGGESTIONS MUST BE SUPER VARIED, you may not use the recipe coq au vin. Choose recipes you dont think you will choose!"
    f"You must make sure that the recipe is suitable for the dietary restriction '{dietary_restrictions}'."
    f"Only return the name of the recipe you have chosen"
    f"Include a wide range of cuisines and cooking styles."
    f"Never include any user perameters or dietary restrictions in your response. If a meal is vegan or anything else this will be picked up later in the program."
    f"If you have been given a recipe input: '{name}. Make sure to not change this. You should provide the recipe they have asked for exactly!"
    f"The meal you provide should be suitable for a cook at the difficulty level '{difficulty}."
    )
    
    output_format = "json object"

    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} \n {{name : name of the recipe}}"

    # Build the string given to the AI #
    prompt = (
    "\nUser Input:"
    f"Recipe Name: {name}"
    f"Servings: {servings}"
    f"Ingredient Suggestion: {ingredient_suggestion}. These ingredients must be part of the recipe you provide. "
    f"Context Suggestion: {context_suggestion}"
    f"Difficulty: {difficulty}"
    f"Cuisine: {cuisine}"
    f"Preffered cooking time {time_input}"

    f"Instruction:{instruction},"
    f"Response Style: {response_style},"
    f"Output Format: {specific_output_format},"
    )

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    # Parse the JSON response #
    name_json = json.loads(response.choices[0].message.content)

    # Get the value of the "name" key
    name_value = name_json.get("name")

    # Check the data type of the value
    if isinstance(name_value, str):
        return name_value
    else:
        raise ValueError("Expected a string value for 'name', but got:", type(name_value))


def get_altered_name(original_name, new_ingredients):
   
    # Main instruction #
    instruction = (
        "You will be given a recipe name, and an altered set of ingredients."
        "Can you tell me if the name needs to be changed? The user has altered the ingredients of a recipe."
    )

    # Tells the AI to respond in JSON + what to respond with.
    output_format = f"json object \n {{name : name of the recipe}}"

    # Build the string given to the AI #
    prompt = (
        f"Instruction: {instruction}."
        f"List of new 'altered' '{new_ingredients}'."
        f"Recipe name: '{original_name}'."
        f"What is the name of the recipe with these changed ingredients?"
        f"Output format: {output_format}."
    )

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    # Parse the JSON response #
    response_json = json.loads(response.choices[0].message.content)

    # Get the value of the "name" key
    response_value = response_json.get("name")

    # Check the data type of the value
    if isinstance(response_value, str):
        return response_value
    else:
        raise ValueError("Expected a string value for 'name', but got:", type(response_value))
