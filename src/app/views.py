import datetime
from flask import render_template, flash, redirect, url_for, g, session, request
from app import app, mongo, lm
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, SelectCategory, MenuCategory, AddExpensesForm
from .user import User


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
        date_now = datetime.datetime.now()
        coll_name = "expense_" + str(date_now.year) + str(date_now.month)
        collection = mongo.db[coll_name]
        add_exp_form = AddExpensesForm()
        form = SelectCategory()
        cat_coll_set = set()
        find_data = collection.find()
        cat_choices = [(x["cat"],x["cat"]) for x in find_data if x["cat"] not in cat_coll_set and not cat_coll_set.add(x["cat"])]
        add_exp_form.category.choices = cat_choices
        cat_choices.insert(0, ("Категория", "Категория..."))
        form.category.choices = cat_choices
        output = []
        summ = 0
        test_data = "Input form: "
        
        if request.method == "POST" and form.submit.data and form.validate_on_submit():
            find_data = collection.find({"cat": form.category.data})
        else:
            find_data = collection.find()

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

    collection = mongo.db[coll_name]
    find_data = collection.find()
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
        user = mongo.db.users.find_one({"_id": form.login.data})
        
        if user and User.validate_login(user['password'], str(form.password.data)):
            user_obj = User(user['_id'])
            login_user(user_obj)
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
def load_user(username):
    u = mongo.db.users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])