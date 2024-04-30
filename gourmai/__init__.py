import os
from importlib import import_module
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Flask #
from flask import Flask, g, session 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Mailman # 
from flask_mailman import Mail
from flask_cors import CORS

# Init objects for app #
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# Google Analytics #
# from flask_track_usage import TrackUsage
# from flask_track_usage.storage.google_analytics import GoogleAnalyticsStorage

# storage = GoogleAnalyticsStorage(account_id=app.config['GOOGLE_ANALYTICS_ACCOUNT'])
# tracker = TrackUsage(app, [storage])


# ??? #
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


# Set up route blueprints #
def register_blueprints(app):
    for module_name in ('auth', 'home', 'canvas', 'meal', 'payments', 'email', 'discovery'):
        module = import_module('gourmai.{}.views'.format(module_name))
        app.register_blueprint(module.blueprint)


# Init DB #
def configure_database(app):

    # Create all tables #
    try:
        db.create_all()
    except Exception as e:
        print('> Error: DBMS Exception: ' + str(e))

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        


# App factory #
def create_app(config, db):
    app = Flask(__name__)

    app.config.from_object(config)
    app.secret_key = "alubfgawoibgabgpas;ouewgp;oasegoaws"

    # JWT Key #
    app.config['JWT_SECRET_KEY'] = 'v[0p9n%&2p3[2oiugbfp02rt9f!8h2m0-mv2(5897yrn2-v]]'
    
    # Configure Fast-mail settings #
    app.config['GOOGLE_ANALYTICS_ACCOUNT'] = 'G-K0178PN5WQ'
    app.config['MAIL_SERVER'] = "smtp.fastmail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "feedback@gourmai.co.uk"
    app.config['MAIL_PASSWORD'] = "c7d2j7p282d7pm5e"
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False

    
    
    with app.app_context():
        register_extensions(app)
        register_blueprints(app)
        configure_database(app)
        mail.init_app(app)
        CORS(app)
        
    return app