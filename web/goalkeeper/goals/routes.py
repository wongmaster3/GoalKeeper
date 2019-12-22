from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from goalkeeper.models import db, User, Goal, Tag, Friend, Notification, Feed, get_friends
from flask import request
from goalkeeper.goals.forms import GoalForm
from datetime import datetime
from sys import stderr
from goalkeeper.categories.tags import is_tag_str, get_tags


goals = Blueprint("goals", __name__, url_prefix="/goals")

@goals.route('/<goalid>', methods=['GET', 'POST'])
@login_required
def goal(goalid):
    # Find the goal in the Goal table
    result = Goal.query.filter(Goal.id == goalid).first()

    if request.method == "POST":
        result.completion = True
        if not result.private_goal:
            post = Feed(
                title= 'Goal Completed: ' + result.description,
                author=current_user.email
            )
            db.session.add(post)
            for friend in get_friends(current_user.email):
                notification = Notification(
                    user_email=friend.email,
                    description=friend.username + " completed their goal: " + result.title,
                    link=url_for('goals.goal', goalid=result.id)
                )
                db.session.add(notification)
        db.session.commit()
        return redirect(url_for("accounts.home"))


    return render_template("goal.html", currentgoal=result, useremail=current_user.email)

@goals.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == "GET":
        # We are retrieving the webpage here
        form = GoalForm()
        return render_template("add_goal.html", form=form)
    else:
        # We are adding goals here
        form = GoalForm()

        goal = Goal(
            user_email=current_user.email,
            title=form.title.data,
            description=form.description.data,
            tags=(form.tags.data if is_tag_str(form.tags.data) else ''),
            private_goal=(form.private_goal is not None and form.private_goal.data)
        )

        # Register a tag
        tags = Tag.query.all()
        for index,tag in enumerate(tags): tags[index] = tag.text.lower()
        for tag in get_tags(form.tags.data):
            # If a tag is not in the tag database, add it
            if not tag.lower() in tags:
                tag = Tag(text=tag)
                db.session.add(tag)

        if form.due_date is not None:
            print(form.due_date)
            if form.due_date.data is not None:
                print(form.due_date.data)
                try:
                    x = float(form.due_date.data) / 1000.0
                    goal.due_date = datetime.fromtimestamp(x)
                except ValueError:
                    pass

        # We are adding to the news feed here
        post = Feed(
            title='New Goal Created: ' + form.description.data,
            author=current_user.email
        )

        db.session.add(goal)
        db.session.add(post)
        friends = get_friends(current_user.email)
        if not goal.private_goal:
            for friend in friends:
                notification = Notification(
                    user_email=friend.email,
                    description=friend.username + " posted a new goal: " + goal.title,
                    link=url_for('goals.goal', goalid=goal.id)
                )
                db.session.add(notification)
        db.session.commit()
        return redirect(url_for("accounts.home"))


# @goals.route('/edit_goal', methods=['GET', 'POST'])
# def edit_goal():
#     if request.method == "GET":
#         # We are retrieving the webpage here
#         form = GoalForm()
#         return render_template("add_goal.html", form=form)
#     else:
#         # We are adding goals here
#         form = GoalForm()
#         goal = Goal(
#             user_email=current_user.email,
#             title=form.title.data,
#             description=form.description.data,
#         )
#         db.session.add(goal)
#         db.session.commit()
#         return redirect(url_for("accounts.home"))