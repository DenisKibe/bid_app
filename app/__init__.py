from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, logging

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

#from app.auth.views import auth_blueprint
#app.register_blueprint(auth_blueprint)
#from app.api.views import api_blueprint
#app.register_blueprint(api_blueprint)