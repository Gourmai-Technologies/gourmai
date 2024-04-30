import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_equipment(method):
    instruction = f"Please provide a list of equipment or utensils typically used in creating the recipe: '{method}'."

    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f"{output_format} {{equipment: [list of equipment items]}}"

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

    # Parse JSON string #
    equipment_json = json.loads(response.choices[0].message.content)

    # Return list of strings #
    equipment_value = equipment_json.get("equipment")

    # Check the data type of the value
    if isinstance(equipment_value, list):
        return equipment_value
    else:
        raise ValueError("Expected a list value for 'equipment', but got:", type(equipment_value))
