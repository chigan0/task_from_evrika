from uuid import uuid4
from hashlib import pbkdf2_hmac

from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, or_, and_

from api.common.models import User


class UserGet(Resource): # Endpoint user get data
	@jwt_required()
	def get(self, user_id):
		if len(user_id) == 36:# Checking the length of the public id
			session = current_app.config['db_connect']
			user_db_data = session.query(User).filter(User.public_id == user_id)

			if user_db_data.count() > 0:
				user_data = user_db_data.first().serialize

				session.close()
				return {'data': user_data}

			session.close()
		return {'results': "User with this user_id not found"}


class UserAdd(Resource): # Endpoint Add user
	@jwt_required()
	def post(self):
		try:
			if get_jwt()['sub']['role'] == "admin": #decrypt jwt token and check sender role
				data = request.get_json()
				session = current_app.config['db_connect']
				dd = session.query(User).filter(or_(
						User.username == data['username'],
						User.email == data['email']
				))# Checking if a user is registered with this email or username
				
				
				if dd.count() == 0:
					user_unique_id = str(uuid4())
					user_data = User(public_id = user_unique_id,
									email = data['email'].replace(' ', ''), 
									username = data['username'],
									role = data['role'] if 'role' in data else 'user')

					user_data.set_password_hash(data['password'].replace(' ', ''), current_app.config['SECRET_KEY'])

					try:
						session.add(user_data)
						session.commit()
						
						session.close()					
						return {"user_unique_id": user_unique_id,}

					except exc.SQLAlchemyError as e:
						current_app.logger.exception(e)
						session.rollback()

				
				session.close()			
				return {"error": "This email address or username is already registered"}

			else:
				return {"error": "You are prohibited This action is"}

		except Exception as e:
			current_app.logger.exception(e)
			return {"error": "No valid JSON"}


class UserAuth(Resource): # Endpoint user Authorization
	def post(self):
		try:
			access_token = ""
			email = request.get_json()['email']
			result = "Invalid email or password"
			password_hash = pbkdf2_hmac('sha256',
				request.get_json()['password'].encode('utf-8'),
				current_app.config['SECRET_KEY'].encode('utf-8'),
				100000).hex()

			session = current_app.config['db_connect']
			user_data = session.query(User).filter(and_(
					User.email == email,
					User.password_hash == password_hash
			))

			if user_data.count() == 1:
				access_token = create_access_token(identity={
					'role': user_data.first().role,
					'public_id': user_data.first().public_id
				}, expires_delta=False)
				result = ""

			session.close()
			return {"result": result, "access_token": access_token}
		
		except Exception:
			current_app.logger.exception(e)
			return {"error": "No valid JSON"}


class SetUserStatus(Resource): # Endpoint Set user Status
	@jwt_required()
	def post(self,):
		try:
			user_id = request.get_json()['user_id']
			new_status = request.get_json()['status']

			if get_jwt()['sub']['role'] == "admin" and len(user_id) == 36:
				session = current_app.config['db_connect']
				user_db_data = session.query(User).filter(User.public_id == user_id)

				if user_db_data.count() > 0:
					old_status = user_db_data.first().status
					user_db_data.first().status = new_status

					session.commit()
					session.close()
					return {"unique_id": user_id,
							"old_status": old_status, "new_status": new_status}

			return {"error": "You are not allowed This action or account does not exist with this public ID"}
		
		except Exception as e:
			current_app.logger.exception(e)
			return {"error": "No valid JSON"}
