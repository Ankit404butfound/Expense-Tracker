# a FLASK APP FOR EXPENSE TRACKING USING SQLITE DATABASE

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy #pip install flask_sqlalchemy
from sqlalchemy import create_engine #pip install sqlalchemy
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

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=5001)
