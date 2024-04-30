import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Returns a list of alternatives when given a single ingredient, response is based on recipe. #
def get_alternative_ingredients(recipe_name, ingredient_name):

    instruction = (
        "An ingredient and recipe name will be provided. You must answer with all suitable substitutions to that ingredient."
        "You should provide the ingredient name with no extra details."
        "Please answer 'No substitutions' if nothing can replace the ingredient in question."
    )

    output_example = "{{ substitutions : ['list of substitutions here'] }}"

    # Full string given to the AI #
    prompt = (
        f"Instruction: {instruction}"
        f"Output example: {output_example}"
        f"Question: Please provide substitutes for the ingredient '{ingredient_name}' that is suitable for the recipe {recipe_name}"
    )

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # Parse JSON string #
    return json.loads(response.choices[0].message.content)
    