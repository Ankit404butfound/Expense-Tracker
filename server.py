# a FLASK APP FOR EXPENSE TRACKING USING SQLITE DATABASE
import os
import atexit

from flask import Flask, render_template, request, redirect, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS 

app = Flask(__name__, template_folder="build/", static_folder="build/static")
sqlite_path = "expense.db"
CORS(
    app,
    origins=["*"],
    )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + sqlite_path

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    purchased_by = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.id
    

def create_backup_of_db():
    data = open("instance/expense.db", 'rb').read()
    with open("../expense_backup.db", 'wb') as f:
        f.write(data)
    print("backup created")

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        item_name = request.form['item_name']
        amount = request.form['amount']
        purchased_by = request.form['purchased_by']
        purchase_date = request.form['purchase_date']
        print(purchase_date)
        purchase_date = " ".join(purchase_date.split(" ")[:4])
        purchase_date = datetime.strptime(purchase_date, '%a %b %d %Y').strftime('%b %d %Y')

        expense = Expense(item_name=item_name, amount=amount, purchased_by=purchased_by, purchase_date=purchase_date)
        db.session.add(expense)
        db.session.commit()
        return "success"
    return "success"


@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get(id)
    if request.method == 'POST':
        expense.item_name = request.form['item_name']
        expense.amount = request.form['amount']
        expense.purchased_by = request.form['purchased_by']
        expense.purchase_date = request.form['purchase_date']
        db.session.commit()
    
    return "success"


@app.route('/delete_expense/<int:id>', methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return "success"


@app.route('/get_expenses')
def get_expenses():
    # expenses = Expense.query.all()
    # json = {
    #     "expenses": []
    # }
    # for expense in expenses:
    #     json["expenses"].append({
    #         "id": expense.id,
    #         "item_name": expense.item_name,
    #         "amount": expense.amount,
    #         "purchased_by": expense.purchased_by,
    #         "purchase_date": expense.purchase_date
    #     })
    # return json

    # Get all expenses of the current month
    current_month = datetime.now().strftime('%b')
    month = request.args.get("month")
    if month:
        current_month = datetime.strptime(month, "%m").strftime("%b")
    expenses = Expense.query.filter(Expense.purchase_date.contains(current_month)).order_by(Expense.purchase_date)
    json = {
        "expenses": []
    }
    for expense in expenses:
        json["expenses"].append({
            "id": expense.id,
            "item_name": expense.item_name,
            "amount": expense.amount,
            "purchased_by": expense.purchased_by,
            "purchase_date": expense.purchase_date
        })

    return json



@app.route('/delete_all')
def delete_all():
    expenses = Expense.query.all()
    for expense in expenses:
        db.session.delete(expense)
        db.session.commit()
    return "success"



@app.route("/calculate_expenses_owed")
def calculate_expenses_owed():
    current_month = datetime.now().strftime('%b')
    month_number = request.args.get("month")
    month = datetime.strptime(month_number, "%m").strftime("%b") if month_number else current_month
    #get sum of all expenses by Ankit in current month
    expenses_by_Ankit = Expense.query.filter(Expense.purchased_by.contains("Ankit"), Expense.purchase_date.contains(month)).with_entities(db.func.sum(Expense.amount)).scalar()
    expenses_by_Ayush = Expense.query.filter(Expense.purchased_by.contains("Ayush"), Expense.purchase_date.contains(month)).with_entities(db.func.sum(Expense.amount)).scalar()
    expenses_by_Dhruv = Expense.query.filter(Expense.purchased_by.contains("Dhruv"), Expense.purchase_date.contains(month)).with_entities(db.func.sum(Expense.amount)).scalar()
    expenses_by_Shubhendra = Expense.query.filter(Expense.purchased_by.contains("Shubhendra"), Expense.purchase_date.contains(month)).with_entities(db.func.sum(Expense.amount)).scalar()

    print(expenses_by_Ankit, expenses_by_Ayush, expenses_by_Dhruv, expenses_by_Shubhendra)
    if expenses_by_Ankit is None:
        expenses_by_Ankit = 0

    if expenses_by_Ayush is None:
        expenses_by_Ayush = 0

    if expenses_by_Dhruv is None:
        expenses_by_Dhruv = 0

    if expenses_by_Shubhendra is None:
        expenses_by_Shubhendra = 0

    total_expenses = expenses_by_Ankit + expenses_by_Ayush + expenses_by_Dhruv + expenses_by_Shubhendra
    expenses_per_person = total_expenses / 4

    Ankit_ows = expenses_per_person - expenses_by_Ankit
    Ayush_ows = expenses_per_person - expenses_by_Ayush
    Dhruv_ows = expenses_per_person - expenses_by_Dhruv
    Shubhendra_ows = expenses_per_person - expenses_by_Shubhendra

    json = {
        "expenses": {
            "Ankit": expenses_by_Ankit,
            "Ayush": expenses_by_Ayush,
            "Dhruv": expenses_by_Dhruv,
            "Shubhendra": expenses_by_Shubhendra
        },
        "average_expenses_per_person": expenses_per_person,
        "expenses_owed": {
            "Ankit": Ankit_ows,
            "Ayush": Ayush_ows,
            "Dhruv": Dhruv_ows,
            "Shubhendra": Shubhendra_ows
        },
        "to_pay": {}
    }
    
    expenses_owed = {
        "Ankit": Ankit_ows,
        "Ayush": Ayush_ows,
        "Dhruv": Dhruv_ows,
        "Shubhendra": Shubhendra_ows
    }

    while any(expenses_owed.values()):
        min_key, min_value = min(expenses_owed.items(), key=lambda item: item[1])
        max_key, max_value = max(expenses_owed.items(), key=lambda item: item[1])

        json["to_pay"][max_key+" to "+min_key] = abs(min_value)
        expenses_owed[max_key] = max_value + min_value
        expenses_owed[min_key] = 0

    return json


@app.route("/listen_to_push_event", methods=["POST"])
def listen_to_push_event():
    print("push event received")
    os.system("git pull") #pull changes from github
    print("changes pulled")
    return "success"


@app.route("/ping")
def ping():
    return "pong"


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_backup_of_db, 'interval', minutes=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run("0.0.0.0", debug=True, port=5002)
