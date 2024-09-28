from app import app
from src.ext import db

with app.app_context():
    db.create_all()