import json

# Flask #
from flask import Flask, current_app
from flask_login import UserMixin

# Gourmai #
from gourmai import db, session

# SQLAlchemy #
from sqlalchemy import LargeBinary, Column, Date
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import column_property

class Recipes(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)

    # Recipe Info # 
    recipe_name = db.Column(db.String)
    method = db.Column(db.ARRAY(db.String))
    summary = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    history = db.Column(db.Text)
    origin = db.Column(db.String)
    cuisine = db.Column(db.String)
    difficulty = db.Column(db.String)
    diet_conclusion = db.Column(db.Text)
    equipment = db.Column(db.ARRAY(db.String))
    allergen_tags = db.Column(db.ARRAY(db.String))
    diet_tags = db.Column(db.ARRAY(db.String))
    date_created = column_property(Column(Date))

    # Relationships #
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe')
    images = db.relationship('Images', backref='recipe', lazy=True)
    nutrition = db.relationship('Nutrition', backref='recipe', lazy=True, uselist=False)
    
    

    @classmethod
    def get_recipe_by_id(cls, session, item_id):
        return session.query(cls).filter_by(id=item_id).first()
    @classmethod
    def return_recent_recipes(cls):
        with current_app.app_context():
            session = db.session()
            recent_recipe_names = session.query(cls.recipe_name).order_by(cls.id.desc()).limit(10).all()
            return [name for (name,) in recent_recipe_names]

class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    # Image in byte64 format # 
    image = db.Column(db.Text)

class Nutrition(db.Model):
    __tablename__ = 'nutrition'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), unique=True)

    # Nutrition Data #
    calories = db.Column(db.String)
    carbohydrates = db.Column(db.String)
    cholesterol = db.Column(db.String)
    total_fat = db.Column(db.String)
    saturated_fat = db.Column(db.String)
    trans_fat = db.Column(db.String)
    fibre = db.Column(db.String)
    protein = db.Column(db.String)
    sodium = db.Column(db.String)
    sugar = db.Column(db.String)
    potassium = db.Column(db.String)

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, index=True)

    # Relationships #
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient')

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    quantity = db.Column(db.String(255))

    # Relationships #
    recipe = db.relationship('Recipes', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')

class BeveragePairing(db.Model):
    __tablename__ = 'beverage_pairings'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    beverage_name = db.Column(db.String(255), nullable=False)
    beverage_description = db.Column(db.Text)

    recipe = db.relationship('Recipes', backref='beverage_pairings')

# Suggestions DB Class #
# This is not necessary. Woops #
class Suggestions(db.Model):
    __tablename__ = 'suggestions'

    id = db.Column(db.Integer, primary_key=True)
    suggestions = db.Column(db.JSON)
    mainsummary1 = db.Column(db.JSON)
    mainsummary2 = db.Column(db.JSON)
    mainsummary3 = db.Column(db.JSON)
    mainsummary4 = db.Column(db.JSON)
    mainsummary5 = db.Column(db.JSON)

    @classmethod
    def get_row_by_id(cls, session, item_id):
        return session.query(cls).filter_by(id=item_id).first()
