from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import Required, EqualTo

class LoginForm(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class SignupForm(FlaskForm):
    login = TextField('Login', validators = [Required()])
    email = TextField('Email Address', validators = [Required()])
    password = PasswordField('New Password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('submit')


class SelectCategory(FlaskForm):
   category = SelectField("Категория")
   submit = SubmitField('submit')


class MenuCategory(FlaskForm):
   month = SelectField("Month")


class AddExpensesForm(FlaskForm):
    sum_uah = TextField('sum_uah', validators=[Required()])
    date = DateField('date')
    category = SelectField('Категория')
    details = TextField('details')
    submit = SubmitField('submit')