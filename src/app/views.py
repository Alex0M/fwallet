import datetime, json
from flask import render_template, flash, redirect, url_for, g, session, request
from app import app, db, lm
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, SignupForm, SelectCategory, MenuCategory, AddExpensesForm
from .models import User, Category, Account, Budget, Operation, OperationType
from sqlalchemy.orm import aliased


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
            pass
        else:
            today = datetime.date.today()
            start_date = datetime.date(today.year, 3, 1)
            output = Operation.query.filter(Operation.date >= start_date).all()

        if request.method == "POST" and add_exp_form.submit.data and add_exp_form.validate_on_submit():
            test_data = test_data + str(add_exp_form.date.data) + " " + str(add_exp_form.category.data) + " " + str(add_exp_form.sum_uah.data) + str(add_exp_form.details.data)
            
        return render_template("index.html", 
                                data = output, 
                                form = form, 
                                total = summ, 
                                add_exp_form = add_exp_form,
                                test_data = test_data)


@app.route('/category', methods = ['GET', 'POST'])
@login_required
def category():
    today = datetime.datetime.now()
    start_date = datetime.date(today.year, 3, 1)
    menu = MenuCategory()
    months_choises = []
    data = {}
    
    for i in range (1,13):
        months_choises.append((str(i), str(datetime.date(today.year, i, 1).strftime('%B'))))
    menu.month.choices = months_choises

    if request.method == 'POST' and menu.validate_on_submit():
        pass
    else:
        category_alias = aliased(Category)
        query_data = db.session.query(db.func.sum(Operation.amount).label("amount"), Category.parent_id, category_alias.name.label("category_name")).join(Category).join(category_alias, Category.parent_category).group_by(Category.parent_id).filter(Operation.date >= start_date).all()
        
        category_data = []

        for value in query_data:
            detail_amount = []
            query_detail_data = db.session.query(db.func.sum(Operation.amount).label("amount"), Category.name).join(Category).filter(Category.parent_id == value.parent_id).group_by(Category.name).all()
            for val in query_detail_data:
                detail_data = {"name": val.name, "amount": float(val.amount)}
                detail_amount.append(detail_data)

            category_data.append({"parent_id": value.parent_id, "name": value.category_name, "amount": float(value.amount), "detailAmount": detail_amount})

        data = {"categories": category_data}
        
    return render_template("category.html", data = data, menu = menu)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
   
    if request.method == 'POST' and form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        registered_user = User.query.filter_by(username=form.login.data).first()

        if registered_user is not None and registered_user.is_correct_password(form.password.data):
            login_user(registered_user)

            return redirect(url_for('index'))
        
        else:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
           
    return render_template("login.html",
            title = "Sign in",
            form = form)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate():
            user = User(username=form.login.data, password=form.password.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for('login'))
        else:
            return render_template("signup.html", form=form)
    
    elif request.method == 'GET':
        return render_template("signup.html", form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('login'))


@app.route('/about')
def about():
    pass


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
