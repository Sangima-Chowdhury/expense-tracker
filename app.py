from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


@app.route("/")
def home():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title")
    amount = request.form.get("amount")

    new_expense = Expense(title=title, amount=float(amount))

    db.session.add(new_expense)
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.get(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5003)
