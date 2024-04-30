import json
import os
import time
import requests
# Gourmai #
from gourmai.meal.get_functions.utils import *
from gourmai.meal.get_functions.image_compression import compress_and_update_images

# OpenAI #
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_image(recipe_name, ingredients):

    
    response_style = "You are a culinary expert providing professional photrealistic photographs."
    try:
        ########## Swtich for image generation in .env ##########
        #image_generation_switch = os.getenv('IMAGE_GENERATION')
        image_generation_switch = True
        
        # Start function timer
        start_time = time.time()

        # Standard instruction/ response set.

        instruction = (
            "You are tasked to provide an image that summarizes the given recipe name in a visually appealing and accurate manner. "
            "You will receive the name of a specific dish, and based on this, you should generate an image that not only represents the dish "
            "but does so in a way that is true to its ingredients, preparation, and serving style. Consider elements like garnishes, plating, "
            "and context to ensure the image is a faithful and attractive representation of the recipe."
        )

        # Default prompt.
        prompt = f"""
        Response Style:{response_style}
        Instruction:{instruction}
        Prompt: Please provide a image of {recipe_name}
        """
        timeout_seconds = 30

        # for switching #
        if image_generation_switch == True:
            
            print("get_image() starting...")
            try:
                response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                )

                # Calculate the elapsed time
                elapsed_time = time.time() - start_time

                # Print details #
                print(f"\nImage generation time: {elapsed_time} seconds")

                # Turn url into html #
                image_base64 = image_to_base64_html(response.data[0].url)
                #print(f"This is the image URL: {response.data[0].url}")
                return image_base64
                
            except Exception as e:
                print(f"Image generation failed.: {e}")
                
                raise e
                
        elif image_generation_switch == False:
            
            print("Image generation turned off.")
            return "NoImage"

    except Exception as e: 
        raise e
        print(f"An error occured: {e}")
        return ("An unexpected error occurred. Please try again later.")
        