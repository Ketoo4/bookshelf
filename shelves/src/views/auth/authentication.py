from flask import render_template, request, Blueprint, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from uuid import uuid4

from src.ext import db
from src.models.user import User
from src.config import Config
from src.views.auth.form import RegisterForm, LoginForm, EditProfileForm


TEMPLATE_FOLDER = path.join(Config.PROJECT_ROOT, "templates")
auth_bp = Blueprint("authentication", __name__, template_folder=TEMPLATE_FOLDER)


# Login
@auth_bp.route("/signin", methods=["POST", "GET"])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if not user:
            flash("User doesn't exist")
            return redirect("/signin")
        
        if user.check_password(form.password.data):
            login_user(user)
        else:
            flash("Incorrect password or username")
            return redirect("/signin")
        
        flash("Login was successfull")
        
        next = request.args.get("next")
        if next:
            return redirect(next)
        else:
            return redirect("/shelves")
    return render_template("signin.html", form=form)

# Logout
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Log out successful")
    return redirect("/")



# Sign up/Register
@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User(first_name=form.first.data, last_name=form.last.data, username=form.username.data, password=form.password.data, email=form.email.data,
                    birthday=form.birthday.data, gender=form.gender.data)
        
        img = form.profile_pic.data
        if img:
            __, extention = path.splitext(img.filename)
            filename = str(uuid4())
            directory = path.join(Config.UPLOAD_FOLDER, f"{filename}{extention}")
            img.save(directory)
            user.profile_pic=f"{filename}{extention}"
        
        user.create()
        
        flash("Registration was successful!")
        return redirect("/")
    return render_template("register.html", form=form)


# edit user profile information
@auth_bp.route("/edit_user", methods=["GET", "POST"])
@login_required
def edit_user():
    # if not current_user.is_admin():
    #    return redirect("/")
    user = User.query.get(current_user.id)
    form = EditProfileForm(first=user.first_name, last=user.last_name, username=user.username, 
                           email=user.email, birthday=user.birthday, gender=user.gender, bio=user.bio)
    if form.validate_on_submit():
        user.first_name=form.first.data
        user.last_name=form.last.data
        user.username=form.username.data
        user.email=form.email.data
        user.birthday=form.birthday.data 
        user.gender=form.gender.data
        user.bio=form.bio.data
        db.session.commit()
        referrer = request.form.get('referrer', '/shelves')
        return redirect(referrer)

    return render_template("edit_profile.html", form=form)


# Change profile picture
@auth_bp.route("/shelves/change_profile_pic", methods=['POST'])
@login_required
def change_profile_picture():
    user = User.query.filter_by(id=current_user.id).first()

    if 'profile_pic' not in request.files:
        flash('No file part')
        return redirect(url_for('shelves'))

    img = request.files['profile_pic']

    if img.filename == '':
        flash('No selected file')
        return redirect(url_for('shelves'))

    if img and allowed_file(img.filename):
        extension = path.splitext(img.filename)[1]
        filename = f"{uuid4()}{extension}"
        directory = path.join(Config.UPLOAD_FOLDER, filename)
        img.save(directory)
        user.profile_pic = filename
        db.session.commit() 
        
        flash('Profile picture updated successfully')
        return redirect("/shelves")

    flash('Invalid file type')
    return redirect("/shelves")

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions