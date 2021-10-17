from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from cafe_form import CafeForm
from flask_sqlalchemy import SQLAlchemy

import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///coffee-and-wifi.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(500), unique=True, nullable=False)
    opening = db.Column(db.String(250), nullable=False)
    closing = db.Column(db.String(250), nullable=False)
    coffee_rating = db.Column(db.String(50), nullable=False)
    wifi_rating = db.Column(db.String(50), nullable=False)
    power_rating = db.Column(db.String(50), nullable=False)


db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_entry = CafeEntry(
            name=request.form["name"],
            location=request.form["location"],
            opening=request.form["opening"],
            closing=request.form["closing"],
            coffee_rating=request.form["coffee_rating"],
            wifi_rating=request.form["wifi_rating"],
            power_rating=request.form["power_rating"]
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_entries = db.session.query(CafeEntry).all()
    return render_template('cafes.html', cafes=all_entries)


if __name__ == '__main__':
    app.run(debug=True)
