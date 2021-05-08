from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, logging
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail


app=Flask(__name__)
app.config.from_object(Config)

#logger
#logging.basicConfig(filename='logs/app.log', format='%(asctime)s-[%(levelname)s]- %(name)s : %(message)s')
#logger=logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
#log=logging.getLogger('werkzeug')
#log.setLevel(logging.CRITICAL)

#db init
db=SQLAlchemy(app)
migrate=Migrate(app, db)
#init Mail
mail = Mail(app)
#init CORS
CORS(app)

from app.routes import initialize_routes

#init jwt
jwt = JWTManager(app)

#init Api
api = Api(app)

initialize_routes(api)