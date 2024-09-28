from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField, DateField, RadioField, SelectField, SubmitField, EmailField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from string import ascii_uppercase, ascii_lowercase, ascii_letters, digits, punctuation
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from datetime import datetime, timedelta


class ShelfForm(FlaskForm):
    shelf_name = StringField("Shelf name")
    submit = SubmitField()
    
class BookForm(FlaskForm):
    title = StringField()
    author = StringField()
    submit = SubmitField()
    