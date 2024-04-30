from flask import current_app, Blueprint

# Register Blueprint #
blueprint = Blueprint(
    'meal_bp',
    __name__,
    url_prefix='/meal'
)