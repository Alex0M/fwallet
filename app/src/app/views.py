import datetime, calendar, json
from flask import render_template, flash, redirect, url_for, g, session, request, jsonify, abort
from app import app, db, lm
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, SignupForm, FilterForm, MenuCategory, AddOperationsForm, AddTransferForm, AddExpensesBudgetForm, AddIncomeBudgetForm, NewAccount
from .models import User, Category, Account, AccountType, Budget, Operation, OperationType, Currency
from sqlalchemy.orm import aliased
import decimal

def updateAccount (account_id, operation_type, operation_value):
    account = Account.query.filter_by(id=account_id).one()
    if operation_type == "expense":
        balance = account.balance - decimal.Decimal(operation_value)
    if operation_type == "income":
        balance = account.balance + decimal.Decimal(operation_value)
    account.balance = balance
    db.session.commit()


def getDescriptionId (description, category):
    cat_des = Category.query.filter(Category.name == description, Category.parent_id != None).first()
    if cat_des is None:
        cat_parent = Category.query.filter(Category.name == category, Category.parent_id == None).first()
        if cat_parent is None:
            cat_parent = Category(parent_id = None, name = category)
            db.session.add(cat_parent)
            db.session.commit()
        cat_des = Category(parent_id = cat_parent.id, name = description)
        db.session.add(cat_des)
        db.session.commit()

    return cat_des.id


def addOpereation (operation_type, form_dec, form_cat, form_acc_id, form_data, form_amount,form_curr_id):
    operationtype = OperationType.query.filter(OperationType.name == operation_type).first()
    des_cat_id = getDescriptionId(form_dec, form_cat)
    operation = Operation(category_id = des_cat_id, 
                          operationtype_id = operationtype.id,
                          account_id = form_acc_id,
                          date = form_data,
                          amount = form_amount,
                          currency_id = form_curr_id)
    updateAccount(form_acc_id, operation_type, form_amount)
    db.session.add(operation)
    db.session.commit()

    return operation.id


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
        add_exp_form = AddOperationsForm()
        add_transfer_form = AddTransferForm()
        accounts = [(i.id, i.name) for i in Account.query.filter(Account.users_id == current_user.id).all()]
        add_exp_form.account.choices = add_transfer_form.account.choices = add_transfer_form.outputaccount.choices = accounts
        currency_group = Currency.query.all()

        accounts_data = db.session.query(Account).join(AccountType).join(Currency).all()

        output = []
        test_data = []
        summ = 0
        today = datetime.date.today()
        start_date = datetime.date(today.year, 3, 1)
        operation_id = 0

        output = Operation.query.filter(Operation.date >= start_date).order_by(-Operation.date).all()

        if request.method == "POST" and add_exp_form.validate_on_submit():
            if "add-expenses" in request.form:
                operation_id = addOpereation("expense", add_exp_form.categorydes.data, add_exp_form.category.data, add_exp_form.account.data, add_exp_form.date.data, add_exp_form.amount.data, format(request.form['currency-id']))
            if "add-incomes" in request.form:
                operation_id = addOpereation("income", add_exp_form.categorydes.data, add_exp_form.category.data, add_exp_form.account.data, add_exp_form.date.data, add_exp_form.amount.data, format(request.form['currency-id']))
        if request.method == "POST" and add_transfer_form.validate_on_submit():
            operation_id = addOpereation("expense", add_transfer_form.categorydes.data, "Transfer", add_transfer_form.account.data, add_transfer_form.date.data, add_transfer_form.amount.data, format(request.form['currency-id']))
            operation_id = addOpereation("income", add_transfer_form.categorydes.data, "Transfer", add_transfer_form.outputaccount.data, add_transfer_form.date.data, add_transfer_form.amount.data, format(request.form['currency-id']))

        test_data = "add transaction - {}".format(operation_id)
            
        return render_template("index.html", 
                                data = output,
                                accounts_data = accounts_data,
                                total = summ, 
                                add_exp_form = add_exp_form,
                                add_transfer_form = add_transfer_form,
                                currency_group = currency_group,
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
    add_acc_form.group.choices = [(i.id, i.name) for i in AccountType.query.all()]
    data = db.session.query(Account).join(AccountType).join(Currency).all()

    
    if request.method == 'POST' and add_acc_form.validate_on_submit() and "add-account" in request.form:
            input_balance_name = "balance_" + add_acc_form.currency.data
            currency_id = Currency.query.filter_by(name=add_acc_form.currency.data).first()
            account = Account(name=add_acc_form.name.data, accounttype_id=add_acc_form.group.data, users_id=current_user.id, balance=request.form[input_balance_name], currency_id=currency_id.id)
            db.session.add(account)
            db.session.commit()
            data = db.session.query(Account).join(AccountType).join(Currency).all()
            return render_template("accounts.html", add_acc_form = add_acc_form, data = data)

    if request.method == 'POST' and add_acc_form.validate_on_submit() and "edit-account" in request.form:
            currency_id = Currency.query.filter_by(name=add_acc_form.currency.data).first()
            account = Account.query.filter_by(id=format(request.form['account-id'])).one()
            account.name = add_acc_form.name.data
            account.accounttype_id = add_acc_form.group.data
            account.currency_id = currency_id.id
            db.session.commit()
            data = db.session.query(Account).join(AccountType).join(Currency).all()    
            return render_template("accounts.html", add_acc_form = add_acc_form, data = data)

    if request.method == 'POST' and add_acc_form.validate_on_submit() and "delete-account" in request.form:
            account = Account.query.filter_by(id=format(request.form['account-id'])).one()
            db.session.delete(account)
            db.session.commit()
            data = db.session.query(Account).join(AccountType).join(Currency).all()       
            return render_template("accounts.html", add_acc_form = add_acc_form, data = data)

    return render_template("accounts.html", add_acc_form = add_acc_form, data = data)


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

    type_to_insert = [AccountType(name="Наличные"), AccountType(name="Банковский счет"), AccountType(name="Депозит"), AccountType(name="Кредит"), AccountType(name="Инвестиции")]
    op_type_to_insert = [OperationType(name="expense"), OperationType(name="income"), OperationType(name="transfer")]
    currency_to_insert = [Currency(name="uah", base=1, rate=1), Currency(name="usd", base=0, rate=25.25), Currency(name="eur", base=0, rate=28)]
    db.session.bulk_save_objects(type_to_insert)
    db.session.bulk_save_objects(op_type_to_insert)
    db.session.bulk_save_objects(currency_to_insert)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/api/v1/category/<cat_type>', methods=['GET'])
def get_category_api(cat_type):
    if cat_type == "parent":
        res = Category.query.filter(Category.parent_id == None).all()
    elif cat_type == "child":
        res = Category.query.filter(Category.parent_id != None).all()
    else:
        abort(404)
    list_des = [r.as_dict() for r in res]
    
    return jsonify(list_des)


@app.route('/api/v1/accounts/<accont_id>', methods=['GET'])
def get_account_api(accont_id):
    account = Account.query.filter(Account.id == accont_id).first_or_404().as_dict()

    return jsonify(account)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
