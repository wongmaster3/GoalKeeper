from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from goalkeeper.accounts.forms import LoginForm, RegisterForm
from goalkeeper.models import db, User, Goal
from flask import request
from goalkeeper.goals.forms import GoalForm
from sys import stderr

accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts.route('/home', methods=['GET'])
@login_required
def home():
    # Home Page only needs to display current goals
    result = Goal.query.filter(Goal.user_email == current_user.email).all()

    storage = []
    for goal in result:
        if goal.completion == False:
            storage.append(goal)
    return render_template('home.html', results=storage)

@accounts.route('/completed_goals', methods=['GET'])
@login_required
def completed_goals():
    result = Goal.query.filter(Goal.user_email == current_user.email).all()

    storage = []
    for goal in result:
        if goal.completion == True:
            storage.append(goal)
    return render_template('completed_goals.html', results=storage)


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            # flash(user.id + " " + user.username + " " + user.email)
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash('Logged in successfully.', 'success')
                # Retrieve lists of goals in account
                return redirect(url_for("accounts.home"))

            flash('Invalid login.', 'danger')
            return redirect(url_for("accounts.login"))
    else:
        return render_template("login.html", form=form)
#
#
@accounts.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    form = LoginForm()
    return render_template("login.html", form=form)


@accounts.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter(User.email == form.email.data).first()
            if user:
                flash('Email already taken.', 'info')
                return render_template("register.html", form=form)

            user = User(
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            flash('New account created successfully.', 'success')
            return render_template("login.html", form=LoginForm())
    else:
        flash("Register Here!", "success")

    return render_template("register.html", form=form)

@accounts.route('/calendar', methods=['GET'])
@login_required
def view_calendar():
    form = GoalForm()
    return render_template("calendar.html", form=form)