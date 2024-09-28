from flask import render_template, request, Blueprint, url_for
from os import path

from src.config import Config

TEMPLATE_FOLDER = path.join(Config.PROJECT_ROOT, "templates")
print(f"TEMPLATE_FOLDER: {TEMPLATE_FOLDER}")
main_bp = Blueprint("main", __name__, template_folder=TEMPLATE_FOLDER)

@main_bp.route("/")
def index():
    css_url = url_for('static', filename='css/style.css')
    print(f'CSS URL: {css_url}')
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")