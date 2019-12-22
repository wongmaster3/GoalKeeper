from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from goalkeeper.models import db, User, Goal, Friend, Feed
from flask import request
from goalkeeper.goals.forms import GoalForm
from datetime import datetime
from sys import stderr

# Feed will have news when someone becomes friends with your friend or
# when a friend creates a new goal or completes a goal.

feed = Blueprint("feed", __name__, url_prefix="/feed")

@feed.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # Find friends of the user
    friend_query1 = Friend.query.filter(Friend.user1_email == current_user.email).with_entities(
    Friend.user2_email.label('user1_email'))
    friend_query2 = Friend.query.filter(Friend.user2_email == current_user.email).with_entities(Friend.user1_email)
    intersection = friend_query1.intersect(friend_query2)
    friends_of_user = User.query.filter(User.email.in_(intersection)).with_entities(User.email)

    # Query the goals completed and created for each friend as well as friend requests
    result = Feed.query.filter(Feed.author.in_(friends_of_user)).order_by(Feed.date_posted.desc())

    return render_template("feed.html", results=result)