import json
import os
import requests

import time
# Gourmai #
#from gourmai.meal.get_functions.utils import *

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


user_input = {
    'recipe_input': '',
    'ingredientSuggestion': '',
    'contextSuggestion': '',
    'difficulty': 'Michelin',
    'cuisine': 'Any',
    'servings' : '1',
    'time' : '30 - 45 mins',
    'dietaryRestrictions' : {''},
    'unit' : 'metric'
    
}

recipe_name = "Pizza"

ingredients = {'High-protein flour': '150g', 'Active dry yeast': '5g', 'Lukewarm water': '100ml', 'Olive oil': '15ml', 'Salt': '1g', 'Sugar': '1g', 'Peel of organic lemon': '~1/2 lemon', 'Crushed San Marzano tomatoes': '80g', 'Fresh basil leaves': '3-4', 'Nutritional yeast': '10g', 'Garlic powder': '1g', 'Oregano': '1g', 'Sea salt': 'Pinch', 'Extra virgin olive oil': '10ml', 'Sliced vegan cheese': '50g', 'Vegan pepperoni slices': '30g', 'Red onion': '1/4', 'Red bell pepper': '1/4', 'Arugula': '10g'}



start_time = time.time()
print(get_image(recipe_name, ingredients))
end_time = time.time()

elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")