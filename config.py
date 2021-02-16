import os

class Config(object):
    SECRET_KEY="\xac\x90\x8bi\x89z\x12P\xb2\x9c\x8cg>\xeaU\x1d\xb5#\xa0\xb8\x08\x9d\xcd\xc9\xc7\x9e1D\xdb;\xe6\xf1]\x8bM'Mc\x80pX#Oo\xb9k0X*\x8a\xcf}\xb2V\x96\xc3\x97!/\x1d\xd4\xf5\x9a\xf7"
    SQLALCHEMY_DATABASE_URI='postgresql://kibe:denis@localhost/bid_app'
    CSRF_ENABLED=True
    DEBUG = False
    UPLOAD_FOLDER='app/statict/uploads/'
    ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '\x0b\x9eoR\x0b\xc5\x9b8>\xee\xbd\x13\x85\x11"\xc6\xa2\x03_\x8f\xa1\xe8\x12\xea!\xd5\xcd\xf8]>6p'
    
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