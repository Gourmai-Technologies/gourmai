from flask import current_app, Blueprint

# Register blueprint #
blueprint = Blueprint(
    'amazon_bp',
    __name__,
    url_prefix='/amazon'
)
