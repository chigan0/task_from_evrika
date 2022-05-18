class Config:
	SECRET_KEY = "kdjlshgb574iog397"
	DEBUG = True
	VERSION = "v1"


class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test_user:Sql_-132442@127.0.0.1:3306/test"
	JWT_SECRET_KEY = "faf3t22g2"


class ProdConfig(Config):
	SQLALCHEMY_DATABASE_URI = ""
	JWT_SECRET_KEY = ""
