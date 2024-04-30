import os, random, string

# Set up global application configuration #
class Config(object):

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Establish a DB connection #
    try:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://qirhsnngcwxhlu:8713babc959b37165e3fb145031ef199769a83985d8b12d6f3dc61869f1f0ef5@ec2-34-226-28-242.compute-1.amazonaws.com:5432/d40bqrqk4vilhp'

    except Exception as e:
        print('> Fatal Error: Failed to connect to postgres db: ' + str(e) )
        raise e


# Production settings #
class ProductionConfig(Config):
    DEBUG = False

    # Security variables #
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # Other env dependent variables #
    IMAGE_GENERATION = True

# Development settings #
class DebugConfig(Config):
    DEBUG = True

    IMAGE_GENERATION = True
    
# Load all configurations #
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}