from os import path
import os

class Config:
    PROJECT_ROOT =  path.abspath(path.dirname(__file__))
    STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "static"))
    UPLOAD_FOLDER = os.path.join(STATIC_ROOT, "uploads")
    SECRET_KEY = "superdupersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PROJECT_ROOT, "database.db")
    