from src.ext import db
from src.models.base import BaseModel


class Shelf(db.Model):
    __tablename__ = "shelf"
    
    id = db.Column(db.Integer, primary_key=True)
    shelf_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    books = db.relationship('Books', backref='shelf', lazy=True)

class Books(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrowed = db.Column(db.Boolean, default=False)
    
