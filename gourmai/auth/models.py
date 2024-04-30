import ast
import json

# Flask #
from flask_login import UserMixin, current_user

# Gourmai #
from gourmai import db, login_manager
from gourmai.auth.util import hash_pass
from gourmai.meal.models import Recipes

# SQLAlchemy #
from sqlalchemy import Table, Column, Integer, ForeignKey, String, ARRAY
from sqlalchemy.orm import relationship


# Recipe-User association table #
user_recipe_association = db.Table('user_recipe_association',
    Column('user_id', db.Integer, ForeignKey('Users.id')),
    Column('recipe_id', db.Integer, ForeignKey('recipes.id'))
)


# User Table #
class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    # Account details #
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.LargeBinary)

    # Verification # 
    tokens = db.Column(db.Integer, default=25, nullable=False)
    verification_token = db.Column(db.String)
    email_verified = db.Column(db.Boolean)

    # Extra user details #
    measurement_units = db.Column(String, default="Metric")

    dietary_restrictions = db.Column(db.String, default='[]')   # Array of strings
    allergens = db.Column(db.String, default='[]')  # Array of strings
    recipes_generated_counter = db.Column(Integer, default=0)
    saved_recipes_counter = db.Column(Integer, default=0)
    shared_recipes_counter = db.Column(Integer, default=0)

    # Relationships #
    recipes = db.relationship('Recipes', secondary=user_recipe_association, backref=db.backref('users', lazy='dynamic'))

    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


    # Example method to add tokens to a user's account
    def add_tokens(user_id, amount):
        user = Users.query.get(user_id)
        if user:
            user.tokens += amount
            db.session.commit()


    # Example method to deduct tokens from a user's account
    def deduct_tokens(user_id, amount):
        user = Users.query.get(user_id)
        if user:
            if user.tokens >= amount:
                user.tokens -= amount
                db.session.commit()


    @staticmethod
    def update_measurement_units(measurement_unit):
        user = Users.query.get(current_user.id)
        
        if user: 
            user.measurement_units = measurement_unit

            # Commit the changes to the database
            db.session.commit()


    @staticmethod
    def increment_recipes_generated_counter(user_id):
        user = Users.query.get(user_id)
        user.recipes_generated_counter += 1
        db.session.commit()
      


@login_manager.user_loader
def user_loader(id):
    id_int = int(id)
    return Users.query.filter_by(id=id_int).first()


@login_manager.request_loader
def request_loader(request):
    return None
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
