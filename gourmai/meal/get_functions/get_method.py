import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def get_method(recipe_name, ingredients, user_input):

    units = user_input['unit']

    instruction = (
        f"Craft a comprehensive and exceptionally clear cooking method for the recipe '{recipe_name}', "
        f"utilizing the ingredients: {', '.join(ingredients)}. The method should be detailed and articulate, "
        "suitable for inclusion in a high-quality cookbook. Please ensure that each step is described "
        "with precision and culinary insight, offering guidance that is both practical and insightful. "
        "provide these in both imperial and metric units for accessibility. The instructions should be "
        "sequential but without step numbering, as this will be added later. Aim for a narrative that "
        "is both engaging and instructive, guiding the user through the cooking process with the expertise "
        "and finesse of a professional chef."
        f"Make sure all measuerements you provide are in the units '{units}"
    )

    example_output = (
        "[step sentance goes here,"
        "step 2 goes here,"
        "and so on]"
    )

    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} {{method: [list of steps]}}"

    # Full string given to the AI #
    prompt = (
    f"Input context: {input_context},"
    f"Instruction:{instruction},"
    f"Expected output {example_output},"
    f"Response Style: {response_style},"
    f"Output Format: {specific_output_format}"
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
    method_json = json.loads(response.choices[0].message.content)

    # Return list of strings # 
    method_value = method_json.get("method")

    # Check the data type of the value
    if isinstance(method_value, list):
        return method_value
    else:
        raise ValueError("Expected a list value for 'method', but got:", type(method_value))
    