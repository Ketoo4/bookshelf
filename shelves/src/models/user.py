from src.ext import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.base import BaseModel

class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    profile_pic = db.Column(db.String)
    bio = db.Column(db.String)
    
    shelves = db.relationship('Shelf', backref='users')
    books = db.relationship('Books', backref='users')
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return current_user.role == "Admin"


    