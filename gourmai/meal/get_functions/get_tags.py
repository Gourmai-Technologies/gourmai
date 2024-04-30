
import concurrent.futures
from openai import OpenAI
import os
import json

# Gourmai #
from gourmai.meal.get_functions.utils import diet_dict, allergen_dict

# Init #
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_diet_tags(ingredients, diet):

    diet_key = list(diet_dict.keys())[0]
    diet_description = list(diet_dict.values())[0]
    

    
    instruction = (
        f"Your task is to answer if the list ingredients list is described by the tag ({diet})"
        f"Do the ingredients ({ingredients}) fit the description {diet}?"
    )

    # Tells the AI to respond in JSON + what to respond with. #
    specific_output_format = f"{{answer : True or False}}"

    # Full string given to the AI #
    prompt = f"""
    Instruction:{instruction},
    Output Format: {specific_output_format},
    """

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # Parse the JSON response #
    response_json = json.loads(response.choices[0].message.content)
    
    if response_json['answer'] == True:
        return True
    else:
        return False


def get_allergen_tags(ingredients, allergen):

    allergen_key = list(allergen.keys())[0]
    allergen_description = list(allergen.values())[0]
    
    response_style = f"Your task is to search for the allergen {allergen_key} in the ingredient list. If you find an ingredient that contains the allergen {allergen_key} please answer True, if not answer False. Please remember that some ingredients that contain {allergen_key} are {allergen_description}."
    
    instruction = (
        f"Does the list ({ingredients}) contain the allergen {allergen_key}?"
        f"Does the list contain any of the suspect ingredients: {allergen_description}?"
        f"Is there any {allergen_key} in any of the ingredients provided?"
        f"Does the list ({ingredients}) contain the allergen {allergen_key} in any of the ingredients?"
    )

    # Tells the AI to respond in JSON + what to respond with. #
    specific_output_format = f"{{'answer' : }}"

    # Full string given to the AI #
    prompt = f"""
    Instruction:{instruction},
    Response Style: {response_style},
    Output Format: {specific_output_format},
    Allergen your searching for in the list: {allergen},
    Ingredients List: {ingredients}
    """

    # Get the response from the model #
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    # Parse the JSON response #
    response_json = json.loads(response.choices[0].message.content)

    # Return bool #
    if response_json['answer'] == True:
        return True
    else:
        return False


def get_tags(ingredients):
    
    
    allergen_tags = []
    diet_tags = []

    ### Remove to reactivate function ###
    # return allergen_tags, diet_tags

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for allergen tags
        allergen_futures = {executor.submit(get_allergen_tags, ingredients, {key: value}): key for key, value in allergen_dict.items()}
        
        # Submit tasks for diet tags
        diet_futures = {executor.submit(get_diet_tags, ingredients, {key: value}): key for key, value in diet_dict.items()}

        # Collect allergen tags results
        for future in concurrent.futures.as_completed(allergen_futures):
            key = allergen_futures[future]
            if future.result():
                allergen_tags.append(key)

        # Collect diet tags results
        for future in concurrent.futures.as_completed(diet_futures):
            key = diet_futures[future]
            if future.result():
                diet_tags.append(key)

    return allergen_tags, diet_tags