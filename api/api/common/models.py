from hashlib import pbkdf2_hmac
from json import dumps

from sqlalchemy import Integer, String, \
    Boolean, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):# User model
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    public_id = Column(String(37), unique = True, nullable = False)
    email = Column(String(70), unique = True, nullable = False)
    username = Column(String(60), unique = True, nullable = False)
    password_hash = Column(String(168), unique = False, nullable = False)
    role = Column(String(36), unique = False, default = 'user')
    status = Column(String(36), unique = False, default = 'offline')
    create_date = Column(DateTime(), default = datetime.now)

    def set_password_hash(self, password, salt):
        key = pbkdf2_hmac('sha256', password.encode('utf-8'),salt.encode('utf-8'), 100000)
        self.password_hash = key.hex()

    @property
    def serialize(self):
        return {
            'public_id': self.public_id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'status': self.status,
            'create_date': dumps(self.create_date, default=str)
        }
