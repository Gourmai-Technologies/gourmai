import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_history(recipe_name):

        instruction = (
            f"Provide a concise yet captivating history of the recipe '{recipe_name}'. Your response should be limited to a few paragraphs. "
            "Focus on the origin of the recipe, its cultural significance, and any notable historical anecdotes. "
            "Your content should be historically accurate, culturally respectful, and rich in storytelling, "
            "drawing the reader into the fascinating background of the dish. Ensure the history is engaging and informative, "
            "balancing detail with brevity. Use paragraph breaks, indicated by <br>, for readability."
        )

        # Tells the AI to respond in JSON + what to respond with.
        specific_output_format = f"{output_format} {{history: concise and engaging history of the recipe}}"

        # Custom response style as a culinary historian.
        response_style = (
            "As a culinary historian, you possess extensive knowledge of global cuisines and their stories. "
            "Your explanations are vivid, accurate, and succinct, capturing the essence of the dish’s history "
            "without overwhelming the reader. Present the history as a short, engaging narrative that enlightens "
            "and entertains."
        )

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
        history_json = json.loads(response.choices[0].message.content)

        # Return String #
        history_value = history_json.get("history")

        # Check the data type of the value
        if isinstance(history_value, str):
            return history_value
        else:
            raise ValueError("Expected a string value for 'history', but got:", type(history_value))