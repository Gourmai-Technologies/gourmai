from flask import current_app, Blueprint

# Register blueprint #
blueprint = Blueprint(
    'discovery_bp',
    __name__,
    url_prefix='/discovery'
)


