from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, SelectField, SubmitField, DateField, HiddenField, RadioField
from wtforms.validators import Required, EqualTo
from .models import User

class LoginForm(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class SignupForm(FlaskForm):
    login = TextField('Login', validators = [Required()])
    email = TextField('Email Address', validators = [Required()])
    password = PasswordField('New Password', [
        Required(),
        EqualTo('confirm', message='Password does not match the confirm password.')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("Account already exists for this email address.")
            return False
        else:
            return True


class FilterForm(FlaskForm):
   filter_form_category = SelectField(coerce=int)
   account = SelectField(coerce=int)
   operationtype = SelectField(coerce=int)
   search = TextField("Поиск по описанию")
   submit = SubmitField('submit')


class MenuCategory(FlaskForm):
   month = SelectField("Month")


class AddExpensesForm(FlaskForm):
    sum_uah = TextField('sum_uah', validators=[Required()])
    date = DateField('date')
    account = SelectField(coerce=int)
    category = TextField('category', validators=[Required()])
    categorydes = TextField('details', validators=[Required()])
    submit = SubmitField('submit')

class AddExpensesBudgetForm(FlaskForm):
    category = TextField('category', validators=[Required()])
    amount = TextField('amount', validators=[Required()])
    operation = HiddenField('operation', default='expense')
    submit = SubmitField('submit')

class AddIncomeBudgetForm(FlaskForm):
    category = TextField('category', validators=[Required()])
    amount = TextField('amount', validators=[Required()])
    operation = HiddenField('operation', default='income')
    submit = SubmitField('submit')

class NewAccount(FlaskForm):
    name = TextField('name', validators=[Required()])
    group = SelectField(coerce=int)
    currency = RadioField('currency', choices=[('uah','Ukrainian Hryvnia'),('usd','US Dollar'),('eur','Euro')])
    visibility = BooleanField('Show on Dashboard', default='checked')
    balance_uah = TextField('balance_uah')
    balance_usd = TextField('balance_usd')
    balance_eur = TextField('balance_eur')