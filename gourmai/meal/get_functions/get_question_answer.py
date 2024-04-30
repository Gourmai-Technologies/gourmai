import json
import os


# Gourmai #
from gourmai.meal.get_functions.utils import *


# OpenAI #
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# User can ask questions about the meal. #
def get_question_answer(question, recipe):
    recipe = (
        f"Recipe that the user is enquiring about:\n"
        f"\nName: {recipe.recipe_name}"
        f"\nSummary: {recipe.summary}"
        f"\nMethod: {recipe.method}"
        f"\nRegion: {recipe.origin}"
        f"\nIngredients: {recipe.ingredients}" 
        f"\nEquipment: {recipe.equipment}" 
        f"\nPreparation Time: {recipe.prep_time}"
        f"\nCooking Time: {recipe.cook_time}"
        f"\nHistory: {recipe.history}"
    
        f"\n\nNutrition:\n"
        f"\nCalories: {recipe.nutrition.calories}"
        f"\nProtein: {recipe.nutrition.protein}"
        f"\nCholesterol: {recipe.nutrition.cholesterol}"
        f"\nTotal Fat: {recipe.nutrition.total_fat}"
        f"\nSaturated Fat: {recipe.nutrition.saturated_fat}"
        f"\nFibre: {recipe.nutrition.fibre}"
        f"\nSodium: {recipe.nutrition.sodium}"
        f"\nCarbohydrates: {recipe.nutrition.carbohydrates}"
        f"\nSugar: {recipe.nutrition.sugar}"
    )
    
    instruction = f"Your task is to answer questions about the recipe that was generated earlier in the program. You must be as helpful and informative as possible in your response. The user will give you a question about the recipe {recipe} and you will need to answer. You must not answer any questions unrelated to the recipe, if an unrelated question is asked you should politly decline the question."

    # Tells the AI to respond in JSON + what to respond with.
    specific_output_format = f" {{answer : }} "

    # Full string given to the AI #
    prompt = f"""
    Input context: {input_context},
    Instruction:{instruction},
    Response Style: {response_style},
    Output Format: {specific_output_format}
    Recipe: {recipe}
    Question: {question}
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
    response_json = json.loads(response.choices[0].message.content)

    # Return only the content of the 'answer' field
    return response_json['answer']
