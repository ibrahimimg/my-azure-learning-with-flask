from registration import app, login_manager, db
from flask import render_template, url_for, redirect, flash, request
from registration import forms
from registration.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash("Invalid login details", "danger")
    return render_template("login.html", form = form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.generate_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.username.data}, You are now a member!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

"""
@app.route("/dashboard")
def dashboard():
"""