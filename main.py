import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use SQLite for local testing
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define a simple model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item_name = request.form.get("name")
        if item_name:
            new_item = Item(name=item_name)
            db.session.add(new_item)
            db.session.commit()
        return redirect("/")
    
    items = Item.query.all()
    return render_template("index.html", items=items)

@app.route("/delete/<int:item_id>")
def delete(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
