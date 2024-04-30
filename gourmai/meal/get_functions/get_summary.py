import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_summary(recipe_name, method):

    
        response_style = "You are a knowledgeable and enthusiastic chef, skilled at explaining recipes in an engaging, vivid, and clear manner. Your descriptions should bring the recipe to life, highlighting the sensory experiences, the textures, aromas, and flavors involved. Think of how commentators on MasterChef would describe the dish, emphasizing its uniqueness and the joy of cooking and tasting it. Your goal is to make the description appealing, accessible, and a bit more detailed, while still concise."

        instruction = f"Provide a detailed yet concise summary of the recipe '{recipe_name}' in one sentence. Make sure to capture the essence of the dish, its preparation method, and the sensory experience it offers, akin to a MasterChef commentator, but with an extra touch of vivid description."

        # Tells the AI to respond in JSON + what to respond with. #
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

        # Parse JSON String #
        summary_json = json.loads(response.choices[0].message.content)

        # Return String #
        summary_value = summary_json.get("summary")

        # Check the data type of the value # 
        if isinstance(summary_value, str):
            return summary_value
        else:
            raise ValueError("Expected a string value for 'summary', but got:", type(summary_value))


def get_concise_summary(recipe_name):

    response_style = "You are a knowledgeable and enthusiastic chef, skilled at explaining recipes in an engaging, vivid, and clear manner. Your descriptions should bring the recipe to life, highlighting the sensory experiences, the textures, aromas, and flavors involved. Think of how commentators on MasterChef would describe the dish, emphasizing its uniqueness and the joy of cooking and tasting it. Your goal is to make the description appealing, accessible, and a bit more detailed, while still concise."

    instruction = f"Provide concise summary of the recipe '{recipe_name}' in one sentence. Make sure to capture the essence of the dish, its preparation method, and the sensory experience it offers, akin to a MasterChef commentator, but with an extra touch of vivid description. It is imperitive that this should be as short as posible and no more than 20 words."


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

    # Parse JSON String #
    summary_json = json.loads(response.choices[0].message.content)

    summary_value = summary_json.get("summary")

    # Check the data type of the value # 
    if isinstance(summary_value, str):
        return summary_value
    else:
        raise ValueError("Expected a string value for 'summary', but got:", type(summary_value))
