import os

class Config(object):
    SECRET_KEY=""
    SQLALCHEMY_DATABASE_URL='postgresql://kibe:denis@localhost/ticket_app'
    CSRF_ENABLED=True
    DEBUG = False
    UPLOAD_FOLDER='app/statict/uploads/'
    ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class productinConfig(Config):
    DEBUG = False

class StagigConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True