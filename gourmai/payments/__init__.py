from flask import current_app, Blueprint

# Register Blueprint #
blueprint = Blueprint(
    'payments_bp',
    __name__,
    url_prefix='/payments'
)