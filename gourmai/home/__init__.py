# Flask #
from flask import Blueprint

# Register Blueprint #
blueprint = Blueprint(
    'home_bp',
    __name__,
    url_prefix=''
)

# ??? #
from . import views