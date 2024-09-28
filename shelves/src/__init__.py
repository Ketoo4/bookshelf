from flask import Flask

from src.admin_views import SecureModelView, UserView, BookView, ShelfView
from src.models import User, Books, Shelf
from src.config import Config
from src.ext import db, migrate, login_manager, admin
from src.views.auth.authentication import auth_bp
from src.views.main.routes import main_bp
from src.views.shelves.routes import shelves_bp

BLUEPRINTS = [auth_bp, main_bp, shelves_bp]

def create_app():
    app = Flask("__name__")
    app.debug = True
    app.config.from_object(Config)
    
    register_blueprints(app)
    register_extensions(app)
    return app

def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
        
        
def register_extensions(app):
    
    db.init_app(app)
    
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = "authentication.signin"
    
    @login_manager.user_loader
    def loadUser(user_id):
        return User.query.get(user_id)
    
    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(ShelfView(Shelf, db.session))    
    admin.add_view(BookView(Books, db.session))    
    
