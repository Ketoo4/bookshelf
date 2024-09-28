from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField, DateField, RadioField, SelectField, SubmitField, EmailField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from string import ascii_uppercase, ascii_lowercase, ascii_letters, digits, punctuation
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from datetime import datetime, timedelta
from flask_login import current_user

from src.models.user import User

class RegisterForm(FlaskForm):
    first = StringField("First name")
    last = StringField("Last name")
    username = StringField("Username", validators=[DataRequired(), 
                                                   length(min=2, max=24)])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), 
                                                     length(min=8, max=64)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), 
                                                                   length(min=8, max=24), 
                                                                   equal_to("password")])
    birthday = DateField("Birth date", validators=[DataRequired()])
    gender = RadioField("Gender", choices=["Male", "Female"], validators=[DataRequired()])
    profile_pic = FileField("Upload a pic", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Register")

    def validate_username(self, field):
        existing_user = User.query.filter(User.username == field.data).first()
        if existing_user:
            raise ValidationError("User with this name already exists")


    def validate_password(self, field):
        contains_uppercase = False
        contains_lowercase = False
        contains_digits = False
        contains_symbols = False
        for character in field.data:
            if character in ascii_uppercase:
                contains_uppercase = True
            
            if character in ascii_lowercase:
                contains_lowercase = True
            
            if character in punctuation:
                contains_symbols = True
            
            if character in digits:
                contains_digits = True

        if not contains_uppercase:
            raise ValidationError("Password needs to contain an upper characters")
        
        if not contains_lowercase:
            raise ValidationError("Password needs to contain a lower characters")
        
        if not contains_digits:
            raise ValidationError("Password needs to contain a digit")
        
        if not contains_symbols:
            raise ValidationError("Password needs to contain a symbol")
    
    def validate_birthday(self, field):
        today = datetime.today().date()
        twelve_years_ago = today - timedelta(days=12*365.25)
        if field.data > twelve_years_ago:
            raise ValidationError("Should be at least 12 years old to register!")
        
        
        
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("password")
    
    def validate_username(self, field):
        existing_user = User.query.filter(User.username == field.data).first()
        if not existing_user:
            raise ValidationError("User with this name doesn't exists")
        
        
class EditProfileForm(FlaskForm):
    first = StringField("First name")
    last = StringField("Last name")
    username = StringField("Username", validators=[DataRequired(), 
                                                   length(min=2, max=24)])
    email = EmailField("Email", validators=[DataRequired()])
    birthday = DateField("Birth date", validators=[DataRequired()])
    gender = RadioField("Gender", choices=["Male", "Female"], validators=[DataRequired()])
    bio = TextAreaField("Bio", validators=[length(max=200)])
    submit = SubmitField("Save")
    
    def validate_username(self, field):
        existing_user = User.query.filter(User.username == field.data).first()
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError("User with this name already exists")

