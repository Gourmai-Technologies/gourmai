import json
import os

# Gourmai #
from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_nutrition(ingredients, recipe_name):

        # Formatts ingredients dictionary into a multiline string for the AI to understand #
        formatted_ingredients = json.dumps(ingredients)

        instruction = (
            "Using a comprehensive nutritional database, calculate the total nutritional information "
            "for the following list of ingredients. Where possible, provide specific values for each "
            "nutritional component (calories, total_fat, saturated_fat, cholesterol, sodium, protein, sugar, fibre, carbohydrates, potassium). Please always use fibre not fiber!"
            "In cases where exact values vary due to ingredient types or preparation methods (like different"
            "types of cheese or crust), provide an estimated range. "
            "DO NOT include measurement units, please provide an integer answer!"
            ". Here are the ingredients:\n"
            "It does not matter if it varies or you dont have enough inforamtion, in this case you will give me a range like shown. The less information you have the wider the values can be. Make sure to always provide values. NO EXTRA INFORMATION WILL BE GIVEN. NUMBERS AND UITS ONLY!!!!"
            f"{formatted_ingredients} The recipe im enquiring about is {recipe_name}."
        )

        # Tells the AI to respond in JSON + what to respond with.
        specific_output_format = f""" 
        {output_format} 
        Here is an example of how you will structure your response. This is the nutritional information for the provided list of ingredients.
        {{nutrition: [
            calories: 100-200,
            total_fat: 1-2,
            saturated_fat: 0.5,
            cholesterol: 5-10,
            sodium: 50-100,
            protein: 3-6,
            fibre: 0.5 - 1,
            potassium: 118- 132,
            carbohydrates: 2.36-3.0,
            sugar: 2-4]
        }}
        """

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
        
        response_json = json.loads(response.choices[0].message.content)
        response_content = response_json.get("nutrition")
        
        # Already JSON dict #
        return response_content
