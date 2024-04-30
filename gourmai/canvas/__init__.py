# Flask #
from flask import current_app, Blueprint


# Register Blueprint # 
blueprint = Blueprint(
    'canvas_bp',
    __name__,
    url_prefix='/canvas'
)
