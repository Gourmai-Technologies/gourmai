import re
from fractions import Fraction
import json
import requests
import base64
from PIL import Image
import io

### Init standard instruction set for ChatGPT ###
input_context = "We're aiming to build an extensive digital cookbook for food enthusiasts. The AI-driven recipes are intended to simplify cooking by giving clear, precise, and easily understandable instructions. "

response_style = "You are a culinary expert providing information about various aspects of recipes. Your responses should be accurate, concise, and professional. Tailor your answer to the specific question, and if the answer is not known or unavailable, please state that clearly. Your responses should be in a format suitable for a professional chef."


output_format = "output will always be given in a json object format!"

allergen_dict = {
    'gluten':'',

    'sulpher dioxide' : '',

    'sulphites': '',

    'celery': '',

    'crustaceans': '', 

    'egg': '', 

    'fish': '', 

    'lupin' : '', 

    'milk': '', 

    'mustard': '', 

    'molluscs' : '', 

    'nuts': '',

    'semame': '',

    'soya': ''
    }


diet_dict = {
    'Mediterranean' : "",

    'Vegetarian' : "",

    'Vegan' : "",

    'Paleo' : "",

    'Ketogenic' : "",

    'Low-Carb' : "",

    'Low-FODMAP' : "",

    'Halal' : "",

    'Kosher' : "",

    'Diabetic-Friendly' : "",

    'Heart-Healthy' :"",

    'High-Protein' : "",

    'Low-Calorie' : "",

    'Anti-Inflammatory' : "",

    'Immune-Boosting' : "",
}

allergen_dict2 = {
    'gluten':'Wheat flour.Whole wheat flour,Wheat bran, Wheat germ, Wheat starch, Wheatberries, Cracked wheat, Durum, Spelt, Semolina, Farina, Kamut, Einkorn, Barley, Barley malt, Barley flour, Barley malt extract, Barley syrup, Rye, Rye flour, Rye bread, Rye extract, Triticale (a cross between wheat and rye), Brewers yeast (can be derived from barley), Farro, Graham flour (usually made from wheat), Couscous (made from wheat), Bulgur (made from wheat), Malt vinegar (made from barley), Wheat-based soy sauce (traditional soy sauce is usually gluten-free, but some varieties may contain wheat)',

    'sulpher dioxide' : 'Dried fruits, wine, fruit juices, canned fruits, fruit concentrates, fruit jams and jellies, maraschino cherries, molasses, pickled foods, certain condiments, dried vegetables, processed meats, potato products, canned coconut milk and cream, instant mashed potatoes, seafood products, baked goods, pre-prepared or pre-packaged meals, beer and cider, medications.',

    'sulphites': 'Dried fruits, wine, fruit juices, canned fruits, fruit concentrates, fruit jams and jellies, maraschino cherries, molasses, pickled foods, certain condiments (e.g., Worcestershire sauce, vinegar), dried vegetables, processed meats, potato products, canned coconut milk and cream, instant mashed potatoes, seafood products, baked goods, pre-prepared or pre-packaged meals, beer and cider, medications.',

    'celery': 'Cooking stocks, soups, stews, sauces, salads (e.g., Waldorf salad), salad dressings, vegetable juices, processed meats (e.g., sausages, hot dogs, deli meats), pickles, condiments (e.g., mustard, some types of relish), spice blends, seasonings, some snack foods (e.g., seasoned chips), some ready meals or pre-packaged foods, and some herbal supplements or medicines.',

    'crustaceans': 'Crab, lobster, shrimp, prawns, crayfish, langoustine, crab paste, crab extract, lobster paste, lobster extract, shrimp paste, shrimp extract, prawn paste, prawn extract, crayfish paste, crayfish extract, crab oil, lobster oil, shrimp oil, prawn oil, crayfish oil, shellfish stock, fish sauce, seafood flavoring, seafood seasoning, seafood extract, surimi (imitation crabmeat), fish balls, fish cakes, some sauces and condiments (e.g., Worcestershire sauce, oyster sauce), some soups and broths, seafood-flavored snacks or chips, and some processed foods or ready-made meals containing seafood or seafood extracts.', 

    'egg': 'Egg (whole, yolk, white), mayonnaise, salad dressings, baked goods (cakes, cookies, bread, pastries), pasta, noodles, batter mixes, custards, puddings, and certain sauces (e.g., hollandaise).', 

    'fish': 'Anchovy, bass, catfish, cod, flounder, grouper, haddock, hake, halibut, mackerel, mahi-mahi, perch, pike, pollock, salmon, sardine, sea bass, shark, snapper, sole, swordfish, tilapia, trout, tuna, whitefish, caviar, fish oil, fish sauce, fish stock, fish extract, surimi (imitation crabmeat), fish balls, fish cakes, Worcestershire sauce, oyster sauce, some soups and broths, some sauces and condiments, some salad dressings, some processed meats (e.g., fish sausages), some processed foods or ready-made meals containing fish or fish extracts.Fish sauce, Worcestershire sauce, oyster sauce, some soups and broths, some sauces and condiments.', 

    'lupin' : 'Lupin flour, lupin beans, lupin seeds, lupin bran, lupin oil, lupin protein, lupin fiber, lupin extract, lupin flakes, lupin starch, lupin gum, lupin hulls, lupin meal, lupin sprouts, lupin-based ingredients (e.g., lupin-based milk substitutes, lupin-based meat substitutes), lupin-derived additives (e.g., lupin protein isolate), lupin-based sauces, lupin-based condiments, lupin-based pasta, lupin-based baked goods.', 

    'milk': 'Milk (whole, skim, low-fat, condensed, evaporated), milk powder, milk solids, milk fat, milk protein, milk derivatives (e.g., milk sugar, lactose), butter, butterfat, buttermilk, ghee, cream, sour cream, yogurt, cheese, cheese powder, cheese curds, cottage cheese, cream cheese, curd, kefir, whey, whey protein, casein, caseinate, lactalbumin, lactoglobulin, lactoferrin, lactulose, lactose-free milk, lactose-free dairy products, milk chocolate, milk solids, milk derivatives (e.g., milk sugar, lactose), powdered milk, condensed milk, evaporated milk, creamers, ice cream, frozen yogurt, sherbet, gelato, custard, pudding, caramel, toffee, nougat, butterscotch, fudge, some baked goods (e.g., cakes, cookies, pastries, bread), some candies, some chocolates, some snack foods (e.g., chips, crackers, popcorn), some sauces and dressings, some soups and broths, some processed meats (e.g., sausages, meatballs), some instant meals and ready-made meals, some seasoning blends, some protein bars and shakes, some dietary supplements.', 

    'mustard': 'Mustard seeds, mustard powder, mustard flour, mustard oil, mustard paste, prepared mustard, mustard sauce, mustard spread, Dijon mustard, yellow mustard, brown mustard, honey mustard, whole grain mustard, mustard pickles, mustard relish, some salad dressings, some marinades, some sauces and condiments (e.g., barbecue sauce, Worcestershire sauce, curry sauce), some pickled foods, some chutneys, some spice blends, some seasoning mixes, some snacks (e.g., flavored chips, pretzels), some prepared meats (e.g., sausages, deli meats), some sandwiches and wraps, some bread and baked goods (e.g., mustard buns, mustard pretzels), and some prepared meals.', 

    'molluscs' : 'Clams, mussels, oysters, scallops, squid, octopus, snails (escargot), abalone, conch, cuttlefish, periwinkles, whelks, mollusc sauce, mollusc extract, some seafood flavoring, some seafood seasoning, some seafood extract, some fish sauce, some Worcestershire sauce, some oyster sauce, some soups and broths, some sauces and condiments, some pasta dishes, some risotto dishes, some paella dishes, some seafood-based snacks or chips, some processed foods or ready-made meals containing molluscs or mollusc extracts.', 

    'nuts': 'Almonds, Almond extract, Almond flour, Almond oil, Amaretto, Brazil nuts, Cashews, Chestnuts, Chestnut flour, Chestnut purée, Coconut, Coconut oil, Coconut milk, Coconut cream, Coconut flour, Coconut water, Coconut sugar, Coconut aminos, Gianduja, Hazelnuts, Hazelnut extract, Hazelnut oil, Macadamia nuts, Marzipan, Nut butters, Nut flours, Nut oils, Nut paste, Nutella, Nougat, Peanut oil, Peanuts, Pecans, Pine nuts, Pistachios, Praline, Walnut oil, Walnuts, Chocolates, Candies, Snack foods, Baked goods, Cereals, Salad dressings, Sauces, Ice cream, Asian dishes, Vegan/vegetarian meat substitutes, Alcoholic beverages.',

    'semame': 'Sesame seeds, sesame oil, tahini, sesame flour, sesame paste, sesame butter, halva, hummus, some bread and baked goods, some sauces and dressings, some Asian dishes, some snack foods, some condiments, some salad dressings, some spreads, some dips, some desserts, some candies, some granola bars, some cereals.',

    'soya': 'Soybeans, soy sauce, tofu, tempeh, edamame, soy milk, soy flour, soy protein, soybean oil, soy lecithin, miso, natto, soy protein isolate, soy protein concentrate, soybean paste, soy nuts, textured vegetable protein (TVP), some Asian dishes, some baked goods, some meat substitutes, some sauces and dressings, some condiments, some soups and broths, some snacks, some cereals.'
    }
diets_dict2 = (
    {'Mediterranean' : 'Focuses on fruits, vegetables, whole grains, fish, and olive oil, while limiting red meat and processed foods.'},

    {'Vegetarian' : ' Excludes meat and fish but may include dairy and eggs.'},

    {'Vegan' : 'Excludes all animal products, including meat, fish, dairy, eggs, and honey.'},

    {'Paleo' : 'Emphasizes foods presumed to be available to Paleolithic humans, such as lean meats, fish, fruits, vegetables, nuts, and seeds, while excluding processed foods, grains, legumes, and dairy.'},

    {'Ketogenic' : 'High-fat, low-carbohydrate diet designed to induce ketosis, a metabolic state in which the body burns fat for fuel.'},

    {'Low-Carb' : 'Similar to the ketogenic diet, but with less strict carbohydrate restrictions.'},

    {'Atkins Diet' : ' A type of low-carbohydrate diet with four phases, focusing on high-protein and high-fat foods.'},

    {'Raw Food' : 'Consists of unprocessed and uncooked whole plant-based foods, usually fruits, vegetables, nuts, and seeds.'},

    {'Low-FODMAP' : 'Reduces intake of fermentable carbohydrates to alleviate symptoms of irritable bowel syndrome (IBS).'},

    {'Halal' : ' Halal refers to foods that are permissible according to Islamic law. This includes specific methods of slaughtering animals and the avoidance of certain prohibited ingredients such as pork and alcohol.'},

    {'Kosher' : 'Kosher dietary laws are based on Jewish dietary guidelines and regulations. Kosher foods adhere to specific preparation methods and ingredient restrictions, such as the separation of meat and dairy products and the exclusion of certain types of animals and their by-products.'},

    {'Diabetic-Friendly' : 'Diabetic-friendly foods are suitable for individuals with diabetes or those seeking to manage blood sugar levels. These foods typically have a low glycemic index, which means they cause a slower rise in blood sugar levels.'},

    {'Heart-Healthy' : 'Heart-healthy foods are beneficial for cardiovascular health and may help reduce the risk of heart disease. They often include fruits, vegetables, whole grains, lean proteins, and healthy fats, while limiting saturated and trans fats, cholesterol, sodium, and added sugars.'},

    {'Weight Loss' : 'Weight loss foods are intended to aid in weight management by promoting satiety, reducing calorie intake, and supporting metabolism. These foods are often high in fiber, protein, and nutrients while being lower in calories and unhealthy fats.'},

    {'High-Protein' : 'High-protein foods contain significant amounts of protein relative to other macronutrients. Protein is essential for building and repairing tissues, maintaining muscle mass, and supporting various bodily functions.'},

    {'Low-Calorie' : 'Low-calorie foods are those that provide relatively few calories per serving. They are commonly consumed as part of a weight loss or calorie-restricted diet, as they help create a calorie deficit while providing essential nutrients.'},

    {'Anti-Inflammatory' : 'Anti-inflammatory foods help reduce inflammation in the body, which is linked to various chronic diseases and conditions. These foods often include fruits, vegetables, whole grains, nuts, seeds, fatty fish, and spices with anti-inflammatory properties.'},

    {'Immune-Boosting' : 'Immune-boosting foods support a healthy immune system by providing essential nutrients such as vitamins, minerals, antioxidants, and phytochemicals. These foods can help strengthen the bodys defenses against infections and illnesses.'},
)
# Multiplies ingredients (always servs 1) by the servings input from the user.
def multiply_ingredients(ingredient_dict, servings):
    multiplied_ingredients = {}
    
    # Convert servings to a numeric value (float or int)
    try:
        servings = float(servings)
        if servings.is_integer():
            servings = int(servings)
    except ValueError:
        # Handle cases where servings is not a valid number
        raise ValueError("Servings must be a numeric value") 

    for ingredient, detail in ingredient_dict.items():
        # Find all numbers in the quantity string
        numbers = re.findall(r'[\d\.\/]+', detail[0])

        # Replace each number with its multiplied value
        multiplied_quantity = quantity
        for number in numbers:
            try:
                # Convert to Fraction for accurate multiplication with fractions
                original_number = Fraction(number)
                multiplied_number = original_number * servings

                # Format the number back to string, converting to mixed fraction if needed
                if float(multiplied_number).is_integer():
                    multiplied_number_str = str(int(multiplied_number))
                else:
                    multiplied_number_str = str(multiplied_number)

                multiplied_quantity = multiplied_quantity.replace(number, multiplied_number_str, 1)
            except ValueError:
                # Handle cases where the number can't be converted to Fraction (rare)
                pass

        multiplied_ingredients[ingredient] = multiplied_quantity
        
    return multiplied_ingredients

def image_to_base64_html(url, quality=60):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Read the image content as bytes
            image_data = response.content

            # Open the image
            with Image.open(io.BytesIO(image_data)) as img:
                # Compress the image
                img_byte_array = io.BytesIO()
                img.save(img_byte_array, format='JPEG', quality=quality, optimize=True)
                # Encode image data as base64
                base64_encoded = base64.b64encode(img_byte_array.getvalue())
                # Convert bytes to string (UTF-8 encoding)
                base64_string = base64_encoded.decode("utf-8")
                # Return HTML <img> tag with src attribute set to base64 string
                return f"data:image/jpeg;base64,{base64_string}"
        else:
            print("Failed to download image:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))
    return None

