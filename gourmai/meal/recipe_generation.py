

import json
import os
from fractions import Fraction

# Gourmai # 
from gourmai.meal.get_functions.utils import *
from gourmai.meal.models import Recipes

# Flask #
from flask import render_template, redirect, request, url_for, g, Response, session, current_app

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_diet_conclusion(recipe_name, method, user_input):

    diet = user_input['diet']

    response_style = "You are a seasoned dietary expert, well-versed in various diets and nutritional needs. Start by understanding the user's dietary requirements, including any allergies, restrictions, or preferences they have. Then, select recipes that align with their specific diet, ensuring that the ingredients and preparation methods adhere to their dietary guidelines. Provide a concise explanations about why the recipe is suitable for their diet, highlighting key nutritional benefits and potential substitutions. Your goal is to guide users toward healthier and more mindful eating choices, making their culinary journey both nutritious and delicious."

    instruction = f"Provide a detailed yet concise conclusion of why the recipe '{recipe_name}' is selected to go with the diet '{diet}' in a sentences. Be as concise as possible with your response, aiming for one sentence."


    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} {{summary: 'summary goes here'}}"

    # Full string given to the AI #
    prompt = f"""
    Input context: {input_context},
    Instruction:{instruction},
    Response Style: {response_style},
    Output Format: {specific_output_format}
    """

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

# Get main suggestion #
def get_main_course_suggestion(user_input):
    
    # Unpack user input #
    name = user_input['recipe_input']
    servings = user_input['servings']
    ingredient_suggestion = user_input['ingredientSuggestion']
    context_suggestion = user_input['contextSuggestion']
    difficulty = user_input['difficulty']
    cuisine = user_input['cuisine']
    diet = user_input['diet']
    
    try:
        user_input = (
            f"Recipe Name Input: {name}"
            f"Servings Input: {servings}"
            f"Ingredients they want included: {ingredient_suggestion}"
            f"Context of the meal: {context_suggestion}"
            f"Difficulty Level: {difficulty}"
            f"Cuisine type/style: {cuisine}"
            f"Diet: {diet}"
        )

        response_style = f"You are a world class chef with a huge knowlage of every dish ever cooked. You love sharing recipes and suggesting dishes for people to cook."

        instruction = f"Your task is to provide recipe suggestions for people based on their perameters. You must give a wide range of recipes that adhere to the users input. You must provide just the name of the recipe. If the recipe type is given you must adhere to this. For example this recipe is {name} and your suggestions must only be variations of this. If the user has specified a diet you must adhere to this religously. The diet the user has suggested is: '{diet}.'"

        # Tells the AI to respond in JSON + what to respond with.
        specific_output_format = f"{output_format} {{suggestion1: , suggestion2: , suggestion3: , suggestion4: , suggestion5: }}"

        # Full string given to the AI #
        prompt = f""" 
        User Input: {user_input}
        Input context: {input_context},
        Instruction:{instruction},
        Response Style: {response_style},
        Output Format: {specific_output_format}
        """

        # Get the response from the model #
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the JSON response
        response_json = json.loads(response.choices[0].message.content)

        return response_json
    except Exception as e:
        # Handle the exception and raise a custom error
        raise Exception(f"An error occurred during suggestion generation: {str(e)}")

# Get main suggestion #
def get_side_suggestion(user_input, main_selection):
    
    try:
        name = user_input['recipe_input']
    except TypeError:
        name = ''

    try:
        servings = user_input['servings']
    except TypeError:
        servings = ''

    try:
        ingredient_suggestion = user_input['ingredientSuggestion']
    except TypeError:
        ingredient_suggestion = ''

    try:
        context_suggestion = user_input['contextSuggestion']
    except TypeError:
        context_suggestion = ''

    try:
        difficulty = user_input['difficulty']
    except TypeError:
        difficulty = ''

    try:
        cuisine = user_input['cuisine']
    except TypeError:
        cuisine = ''

    try:
        user_input = (
            f"Recipe Name Input: {name}"
            f"Servings Input: {servings}"
            f"Ingredients they want included: {ingredient_suggestion}"
            f"Context of the meal: {context_suggestion}"
            f"Difficulty Level: {difficulty}"
            f"Cuisine type/style: {cuisine}"
        )

        response_style = f"You are a world class chef with a huge knowlage of every dish ever cooked. You love sharing recipes and suggesting dishes for people to cook."

        instruction = f"Your task is to provide recipe suggestions for people based on their perameters. You must give a wide range of sides that adhere to the users input and the recipe they have selected. You must provide just the name of the side. If the recipe type is given you must adhere to this. For example this recipe is {main_selection} and your suggestions must only be variations of this."

        # Tells the AI to respond in JSON + what to respond with.
        specific_output_format = f"{output_format} {{side1: , side2: , side3: , side4: , side5: }}"

        # Full string given to the AI #
        prompt = f""" 
        User Input: {user_input}
        Input context: {input_context},
        Instruction:{instruction},
        Response Style: {response_style},
        Output Format: {specific_output_format}
        """

        # Get the response from the model #
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the JSON response
        response_json = json.loads(response.choices[0].message.content)

        return response_json
    except Exception as e:
        # Handle the exception and raise a custom error
        raise Exception(f"An error occurred during suggestion generation: {str(e)}")
