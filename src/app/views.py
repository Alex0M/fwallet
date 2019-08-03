import datetime, calendar, json
from flask import render_template, flash, redirect, url_for, g, session, request, jsonify, abort
from app import app, db, lm
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, SignupForm, FilterForm, MenuCategory, AddExpensesForm, AddExpensesBudgetForm, AddIncomeBudgetForm, NewAccount
from .models import User, Category, Account, Budget, Operation, OperationType
from sqlalchemy.orm import aliased


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
        add_exp_form = AddExpensesForm()

        def append_choices(list_, query):
            for value in query:
                list_.append((value.id, value.name))

            return list_

 #       add_exp_form.account.choices = append_choices([(0, "Все счета")], Account.query.all())
        add_exp_form.account.choices = [(0, "Все счета")]

        output = []
        test_data = []
        summ = 0
        today = datetime.date.today()
        start_date = datetime.date(today.year, 3, 1)

        output = Operation.query.filter(Operation.date >= start_date).order_by(-Operation.date).all()

        if request.method == "POST" and add_exp_form.submit.data and add_exp_form.validate_on_submit():
            cat_des = Category.query.filter(Category.name == add_exp_form.categorydes.data, Category.parent_id != None).first()
            if cat_des is None:
                cat_parent = Category.query.filter(Category.name == add_exp_form.category.data, Category.parent_id == None).first()
                if cat_parent is None:
                   cat_parent = Category(parent_id = None, name = add_exp_form.category.data)
                   db.session.add(cat_parent)
                   db.session.commit()
                cat_des = Category(parent_id = cat_parent.id, name = add_exp_form.categorydes.data)
                db.session.add(cat_des)
                db.session.commit()
            operation = Operation(category_id = cat_des.id, 
                                  operationtype_id = 1, 
                                  account_id = current_user.id,
                                  date = add_exp_form.date.data,
                                  amount = add_exp_form.sum_uah.data,
                                  currency = 1)
            db.session.add(operation)
            db.session.commit()               
            test_data = "add transaction - {}".format(operation.id)
            
        return render_template("index.html", 
                                data = output, 
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


@app.route('/budget', methods = ['GET', 'POST'])
@app.route('/budget/<month_num>', methods = ['GET', 'POST'])
@login_required
def budget(month_num = datetime.datetime.now().month):
    months = []
    data = {}
    num_days = calendar.monthrange(datetime.datetime.now().year, int(month_num))[1]
    start_date = datetime.date(datetime.datetime.now().year, int(month_num), 1)
    end_date = datetime.date(datetime.datetime.now().year, int(month_num), num_days)
    month_stamp = str(datetime.datetime.now().year) + str(month_num)
    form = AddExpensesBudgetForm()
    form_inc_budget = AddIncomeBudgetForm()
    test_data = ""

    def add_budget_limits(limit, month_stamp, category_name, operationtype_id):
        cat_parent = Category.query.filter(Category.name == category_name, Category.parent_id == None).first()
        if cat_parent is None:
            cat_parent = Category(parent_id = None, name = category_name)
            db.session.add(cat_parent)
            db.session.commit()
        get_budget = Budget.query.filter(Budget.category_id == cat_parent.id, Budget.month_stamp == month_stamp).first()
        if get_budget is None:
            budget = Budget(category_id = cat_parent.id,
                            limit = limit,
                            month_stamp = month_stamp,
                            operationtype_id = operationtype_id)
            db.session.add(budget)
            db.session.commit()
            return True
        else:
            return False


    for i in range (1,13):
        if i == int(month_num):
            months.append((str(i), str(datetime.date(datetime.datetime.now().year, i, 1).strftime('%B')), True))
        else:
            months.append((str(i), str(datetime.date(datetime.datetime.now().year, i, 1).strftime('%B')), False))
    
    income_budget_data = db.session.query(Budget).join(OperationType).join(Category).filter(Budget.month_stamp == month_stamp, OperationType.name == "income").all()
    income_budget_sum = db.session.query(db.func.sum(Budget.limit).label('income_budget_sum')).join(OperationType).filter(Budget.month_stamp == month_stamp, OperationType.name == "income").first()

    expense_budget_data = db.session.query(Budget).join(OperationType).filter(Budget.month_stamp == month_stamp, OperationType.name == "expense").all()
    expense_budget_sum_plan = db.session.query(db.func.sum(Budget.limit).label('expense_budget_sum_plan')).join(OperationType).filter(Budget.month_stamp == month_stamp, OperationType.name == "expense").first()

    category_alias = aliased(Category)
    query_data = db.session.query(db.func.sum(Operation.amount).label("amount"), Category.parent_id, category_alias.name.label("category_name")).join(Category).join(category_alias, Category.parent_category).group_by(Category.parent_id).filter(Operation.date >= start_date, Operation.date <= end_date).all()

    for value in expense_budget_data:
        data[value.category.name] = {"plan": value.limit, "fact": float(0)}
        for value_operation in query_data:
            if value.category.name == value_operation.category_name:
                data[value.category.name] = {"plan": value.limit, "fact" : float(value_operation.amount)}
                query_data.remove(value_operation)
                break

    for value in query_data:
        data[value.category_name] = {"plan": 0, "fact": value.amount}

    if request.method == 'POST' and form.validate_on_submit():
        operation_type = OperationType.query.filter(OperationType.name == form.operation.data).first()
        if add_budget_limits(form.amount.data, month_stamp, form.category.data, operation_type.id):
            return redirect(url_for('budget', month_num = month_num))
        else:
            flash('Looks like you try to add exist category.')

    return render_template("budget.html", data = data,
                                          expense_budget_sum_plan = float(expense_budget_sum_plan[0]),
                                          income_data = income_budget_data,
                                          income_budget_sum = float(income_budget_sum[0]),
                                          months = months, 
                                          test_data = float(income_budget_sum[0]),
                                          form = form,
                                          form_inc_budget = form_inc_budget)


@app.route('/accounts', methods = ['GET', 'POST'])
def accounts():
    add_acc_form = NewAccount()
    add_acc_form.group.choices = [(0, "Наличные")]
    
    if request.method == 'POST' and add_acc_form.validate_on_submit():
        flash('Looks like you try to add account.')
        return render_template("accounts.html", add_acc_form = add_acc_form)

    return render_template("accounts.html", add_acc_form = add_acc_form)


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


@app.route('/dbup')
def dbup():
    db.create_all()

    return redirect(url_for('login'))


@app.route('/api/v1.0/category/<cat_type>', methods=['GET'])
def get_category_api(cat_type):
    if cat_type == "parent":
        res = Category.query.filter(Category.parent_id == None).all()
    elif cat_type == "child":
        res = Category.query.filter(Category.parent_id != None).all()
    else:
        abort(404)
    list_des = [r.as_dict() for r in res]
    
    return jsonify(list_des)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
