import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

# Gourmai #
from gourmai.config import config_dict
from gourmai import create_app, db

from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

# WARNING: Don't run with debug turned on in production! #
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration # 
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load env Config #
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# Run app factory #
app = create_app(app_config, db)

# ??? #
Migrate(app, db)


# ??? #
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)


if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )


### Run App Object ###
if __name__ == "__main__":
    app.run(debug=True)