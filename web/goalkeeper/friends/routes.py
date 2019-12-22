from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from goalkeeper.accounts.forms import LoginForm, RegisterForm
from goalkeeper.models import db, User, Friend, Goal, Notification, Feed
from flask import request
from goalkeeper.goals.forms import GoalForm
from sys import stderr
from sqlalchemy import or_
from sqlalchemy.orm import aliased

friends = Blueprint("friends", __name__, url_prefix="/friends")


@friends.route('/list_friends', methods=['GET'])
@login_required
def list_friends():
    # Return list of all friends and people on the platform
    friend_query1 = Friend.query.filter(Friend.user1_email == current_user.email).with_entities(Friend.user2_email.label('user1_email'))
    friend_query2 = Friend.query.filter(Friend.user2_email == current_user.email).with_entities(Friend.user1_email)
    intersection = friend_query1.intersect(friend_query2)
    union = friend_query1.union_all(friend_query2)
    pending_set_receive = friend_query2.except_(intersection)
    pending_set_sent = friend_query1.except_(intersection)
    friends_of_user = User.query.filter(User.email.in_(intersection)).all()
    not_friends_of_user = User.query.filter(~User.email.in_(union)).filter(User.email != current_user.email).all()
    receive = User.query.filter(User.email.in_(pending_set_receive)).all()
    sent = User.query.filter(User.email.in_(pending_set_sent)).all()
    return render_template("friends_list.html", friends=friends_of_user, find_friends=not_friends_of_user, pending_receive=receive, pending_sent=sent)


@friends.route('/add_friend/<friendemail>', methods=['GET'])
@login_required
def add_friend(friendemail):
    # Add Friend to a table
    friend = Friend(
        user1_email=current_user.email,
        user2_email=friendemail,
    )

    # Check if user is accepting friend request
    # We know that if the current user email and friend email are
    # already in the table, then we know that they became friends.
    if Friend.query.filter(Friend.user2_email == current_user.email).filter(Friend.user1_email == friendemail).first():
        post1 = Feed(
            title=friendemail + ' and ' + current_user.email + ' became friends!',
            author=current_user.email
        )

        post2 = Feed(
            title=friendemail + ' and ' + current_user.email + ' became friends!',
            author=friendemail
        )
        db.session.add(post1)
        db.session.add(post2)

    db.session.add(friend)
    if len(Friend.query.filter(Friend.user1_email == friendemail).all()) > 0:
        notification = Notification(
            user_email=friendemail,
            description=current_user.username + " accepted your friend request!",
            link=url_for('friends.list_friends')
        )
        db.session.add(notification)
    else:
        notification = Notification(
            user_email=friendemail,
            description=current_user.username + " sent you a friend request!",
            link=url_for('friends.list_friends')
        )
        db.session.add(notification)
    db.session.commit()

    return redirect(url_for('friends.list_friends'))

@friends.route('/view_profile/<friendemail>', methods=['GET'])
@login_required
def view_profile(friendemail):
    # Return Profile of User
    goals_of_user = Goal.query.filter(Goal.user_email == friendemail)
    complete_goals_of_user = goals_of_user.filter(Goal.completion == True).filter(Goal.private_goal == False).all()
    uncomplete_goals_of_user = goals_of_user.filter(Goal.completion == False).filter(Goal.private_goal == False).all()
    user = User.query.filter(User.email == friendemail).first()
    return render_template('profile.html', friend_user=user, completed_goals=complete_goals_of_user, uncompleted_goals=uncomplete_goals_of_user)

