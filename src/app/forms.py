from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SelectCategory(FlaskForm):
   category = SelectField("Категория")