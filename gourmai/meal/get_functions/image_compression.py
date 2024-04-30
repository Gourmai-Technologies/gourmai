import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

# Flask #
from flask import Flask
from flask_login import UserMixin


# SQLAlchemy #
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy

import base64
from PIL import Image
import io

def compress_and_convert_to_base64(image_base64, max_size=(1024, 1024), quality=60):
    try:
        # Decode base64-encoded image data
        image_data = base64.b64decode(image_base64)
        
        # Open the image from bytes
        with Image.open(io.BytesIO(image_data)) as img:
            # Resize the image to fit within the specified maximum dimensions
            img.thumbnail(max_size, Image.ANTIALIAS)
            # Convert image to bytes
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='JPEG', quality=quality)
            # Encode the image bytes to base64
            compressed_image_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
            return compressed_image_base64
    except Exception as e:
        print(f"An error occurred while compressing and converting the image: {e}")
        # Log the problematic image data for further investigation
        print("Problematic image data:", image_base64)
        raise e

def compress_and_update_images():
    try:
        # Create SQLAlchemy engine
        engine = create_engine('postgresql+psycopg2://qirhsnngcwxhlu:8713babc959b37165e3fb145031ef199769a83985d8b12d6f3dc61869f1f0ef5@ec2-34-226-28-242.compute-1.amazonaws.com:5432/d40bqrqk4vilhp')
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query all recipes with non-empty image field
        recipes_with_images = session.query(Recipe).filter(Recipe.image != None).all()

        # Iterate through each recipe
        for recipe in recipes_with_images:
            try:
                # Check if image data is valid
                if recipe.image == "An unexpected error occurred. Please try again later.":
                    print(f"Skipping image for recipe with ID {recipe.id}: {recipe.image}")
                    continue  # Skip processing this image
                    
                # Compress and convert image
                compressed_image_base64 = compress_and_convert_to_base64(recipe.image)
                
                # Update the recipe's image field with the compressed version
                recipe.image = compressed_image_base64
                
                # Commit the changes to the database
                session.commit()
                
                print(f"Compressed and updated image for recipe with ID {recipe.id}")
            except Exception as e:
                session.rollback()
                print(f"Error compressing image for recipe with ID {recipe.id}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the session
        session.close()

# # Call the function to compress and update images
# try:
#     compress_and_update_images()   
#     print("images compressed") 
# except Exception as e:
#     raise e