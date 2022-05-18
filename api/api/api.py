import logging

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.orm import Session

from config import Config, TestConfig, ProdConfig
from api.resources.user import UserGet, UserAdd, UserAuth, SetUserStatus
from api.common.db import db_connect, create_table

logging.basicConfig(filename='logs/demo.log', 
	level=logging.DEBUG,  # Setings logging 
	format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.config.from_object(TestConfig if Config.DEBUG else ProdConfig)
api = Api(app)
jwt = JWTManager(app)
engine = db_connect(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['db_connect'] = session = Session(bind = engine)


CORS(app)
create_table(engine) # function to create a table User


api.add_resource(UserGet, f"/{app.config['VERSION']}/user/get/<string:user_id>", methods=['GET'])# Get user data route
api.add_resource(UserAdd, f"/{app.config['VERSION']}/user/registration", methods=['POST']) # User registration route
api.add_resource(UserAuth, f"/{app.config['VERSION']}/user/authorization", methods=['POST']) # authorization route
api.add_resource(SetUserStatus, f"/{app.config['VERSION']}/user/status", methods=['POST']) # Set status route