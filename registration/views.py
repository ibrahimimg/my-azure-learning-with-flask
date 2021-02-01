from registration import app
from flask import render_template, url_for, redirect, flash
from . import forms

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template("login.html", form = form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash(f"Welcome {form.username.data}, You are now a member!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", form = form)