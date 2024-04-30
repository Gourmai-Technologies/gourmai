from flask import current_app, Blueprint

# Register blueprint #
blueprint = Blueprint(
    'auth_bp',
    __name__,
    url_prefix='/auth'
)
