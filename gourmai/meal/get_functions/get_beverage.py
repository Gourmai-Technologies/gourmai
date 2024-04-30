import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Gives the user a short list of beverages that complement the meal. #
def get_beverage(recipe_name, ingredients):

    instruction = f"Generate a list of beverages that would pair well with '{recipe_name}', the ingredients are '{ingredients}'. Include a variety of options such as alcoholic and non-alcoholic beverages, specifying choices for cuisine, what sort of dish it is and anything else that might match a drink and meal perfectly. You should provide a small description of why each of your selections are the what they are."

    # Custom response style as a culinary historian.
    response_style = (
        "As a seasoned beverage connoisseur, your recommendations exude sophistication and expertise. Craft your suggestions with a focus on flavor profiles, pairing nuances, and sensory experiences. Delve into the complexities of each beverage, describing their aromas, tastes, and how they harmonize with the dish, elevating the dining experience to a new level of refinement."
    )

    output_example = "{Cabernet Sauvignon : Reasons why it pairs with meal, another drink : reasons why it pairs with meal}"

    # Full string given to the AI #
    prompt = (
    f"Input context: {input_context},"
    f"Instruction:{instruction},"
    f"Response Style: {response_style},"
    f"Expected output format: {output_example}"
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
