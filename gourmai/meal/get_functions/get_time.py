import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_time(method):

        instruction = f"Please provide the estimated preparation time for the recipe or method: '{method}'. Your response must be given as an integer, no words! Give your answer in minutes."  

        # Tells the AI to respond in JSON + what to respond with.
        specific_output_format = f"{output_format} {{prep_time : int(prep_time), cook_time : int(cook_time), total_time : int(total_time)}}]"

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

        # Parse the JSON response #
        times_json = json.loads(response.choices[0].message.content)

        prep_time = times_json.get("prep_time")
        cook_time = times_json.get("cook_time")
        total_time = times_json.get("total_time")
        
        return prep_time, cook_time, total_time

