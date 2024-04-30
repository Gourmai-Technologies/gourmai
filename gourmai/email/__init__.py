from flask import current_app, Blueprint
from gourmai.canvas.forms import ContactUsForm

# Register blueprint #
blueprint = Blueprint(
    'email_bp',
    __name__,
    url_prefix='/email'
)
