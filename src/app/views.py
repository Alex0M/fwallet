import datetime
from flask import render_template, flash, redirect, url_for, g, session, request
from app import app, db, lm
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, SelectCategory, MenuCategory, AddExpensesForm
from .models import User


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
        add_exp_form = AddExpensesForm()
        form = SelectCategory()

        cat_choices = [("Категория", "Категория...")]
        form.category.choices = cat_choices
        add_exp_form.category.choices = cat_choices
        output = []
        summ = 0
        test_data = "Input form: "
        
        if request.method == "POST" and form.submit.data and form.validate_on_submit():
            find_data = {}
        else:
            find_data = {}

        if request.method == "POST" and add_exp_form.submit.data and add_exp_form.validate_on_submit():
            test_data = test_data + str(add_exp_form.date.data) + " " + str(add_exp_form.category.data) + " " + str(add_exp_form.sum_uah.data) + str(add_exp_form.details.data)

        for coll in find_data:
            summ += int(coll["uah"])
            output.append(coll)

        test_data = str(add_exp_form.errors) + "  " + str(add_exp_form.submit.data)    
        
        return render_template("index.html", 
                                data = output, 
                                form = form, 
                                total = summ, 
                                add_exp_form = add_exp_form,
                                test_data = test_data)

#@app.route('/category')
@app.route('/category', methods = ['GET', 'POST'])
@login_required
def category():
    date_now = datetime.datetime.now()
    menu = MenuCategory()
    months_choises = []
    
    for i in range (1,13):
        months_choises.append((str(i), str(datetime.date(date_now.year, i, 1).strftime('%B'))))
    menu.month.choices = months_choises

    if request.method == 'POST' and menu.validate_on_submit():
        coll_name = "expense_" + str(date_now.year) + str(menu.month.data)
    else:
        coll_name = "expense_" + str(date_now.year) + str(date_now.month)

    find_data = {}
    cat_value = {}

    for coll in find_data:
        if coll["cat"] not in cat_value:
            cat_value[coll["cat"]] = 0
        val = int(cat_value.get(coll["cat"])) + int(coll["uah"])
        cat_value.update({coll["cat"] : val})

    return render_template("category.html", data = cat_value, menu = menu)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
   
    if request.method == 'POST' and form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        password = User.password_hash(str(form.password.data))
        registered_user = User.query.filter_by(username=form.login.data, password=password).first()
        
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login', _external=True))
        
        login_user(registered_user)
        return redirect(url_for('index'))
    
    return render_template("login.html",
            title = "Sign in",
            form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    pass

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
