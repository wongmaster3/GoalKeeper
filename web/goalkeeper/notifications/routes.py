from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from goalkeeper.accounts.forms import LoginForm, RegisterForm
from goalkeeper.models import db, User, Friend, Notification, Goal
from flask import request
from goalkeeper.goals.forms import GoalForm
from sys import stderr
from sqlalchemy import or_
from datetime import datetime, timedelta

notifications = Blueprint("notifications", __name__, url_prefix="/notifications")


@notifications.route('/list_notifications', methods=['GET'])
@login_required
def list_notifications():
    # Return list of all notifications
    goals = Goal.query.filter(
        Goal.due_date is not None,
        Goal.due_date - datetime.now() < timedelta(days=3),
        Goal.due_date - datetime.now() >= timedelta(days=0)
    ).all()
    for goal in goals:
        t = goal.due_date - datetime.now()
        daystring = "tomorrow: " if t.days + 1 == 1 else "in " + str(t.days + 1) + " days: "
        notification = Notification(
            user_email=current_user.email,
            description="You have a goal coming up " + daystring + goal.title,
            link=url_for('goals.goal', goalid=goal.id)
        )
        db.session.add(notification)
    db.session.commit()
    notifications_query = Notification.query.filter(Notification.user_email == current_user.email)
    unread_notes = notifications_query.filter(Notification.clicked == False).all()
    return render_template("notifications.html", notifications_list=unread_notes)

