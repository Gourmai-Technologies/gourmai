import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_origin(recipe_name):
 
    # Tell the AI to respond specifically with the origin.
    instruction = f"Please provide the country or region of origin for the recipe '{recipe_name}'. Your response should be accurate and informative."


    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} {{origin: country or reigon}}"

    # Custom response style, for accuracy. #
    response_style = "You are a culinary expert with extensive knowledge about the origins of dishes from around the world. Your few line answer should be no more than a few words and detail which country or reigon the dish originated. If the awnser is not known you need to state that. Double check your answer. You must only give a couple of words at most."

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
    # Parse the JSON response
    origin_json = json.loads(response.choices[0].message.content)

    origin_value = origin_json.get("origin")

    # Check the data type of the value
    if isinstance(origin_value, str):
        return origin_value
    else:
        raise ValueError("Expected a string value for 'origin', but got:", type(origin_value))