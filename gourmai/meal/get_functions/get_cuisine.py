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

def get_cuisine(recipe_name):

    response_style = "You are a chef tasked souly with supplying the cuisine of  recipe names."
    
    instruction = (
        f"Please provide the cuisine of the recipe {recipe_name}."
    )
    
    output_format = "json object"

    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} \n {{cuisine : cusine of the recipe}}"

    # Build the string given to the AI #
    prompt = (
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
    cuisine_json = json.loads(response.choices[0].message.content)

    # Get the value of the "cuisine" key
    cuisine_value = cuisine_json.get("cuisine")

    # Check the data type of the value
    if isinstance(cuisine_value, str):
        return cuisine_value
    else:
        raise ValueError("Expected a string value for 'cuisine', but got:", type(cuisine_value))
