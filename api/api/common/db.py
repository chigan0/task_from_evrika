from sqlalchemy import create_engine

from config import TestConfig


def db_connect(config): # Connect db function 
	engine = create_engine(config)
	engine.connect()

	return engine


def create_table(engine): # Create table function 
	from api.common.models import User,Base

	Base.metadata.create_all(engine)
