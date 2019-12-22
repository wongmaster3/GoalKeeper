import json

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from goalkeeper.models import db, ForumPost, User, Notification, get_friends
from goalkeeper.categories.tags import is_tag_str, get_tags
from datetime import datetime

forum = Blueprint("forum", __name__, url_prefix="/forum")

time_format = "%Y-%m-%dT%H:%M:%S Z"

@forum.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "GET":
        posts = ForumPost.query.filter(ForumPost.reply_to == None).all()
        data = []
        for post in posts:
            p = {}
            p['id'] = post.id
            p['title'] = post.title
            p['author'] = post.author
            p['tags'] = (json.loads(post.tags) if not post.tags else "")
            p['posts'] = post.posts
            p['views'] = post.views
            p['activity'] = post.last_edited.strftime(time_format)
            data.append(p)
        return render_template('forum/home.html', posts=data)
    elif request.method == "POST":
        if not request.form['title']:
            flash("A title is required to submit a post!")
            flash("Extra")
            return redirect(url_for('forum.home'))
        if not request.form['post']:
            flash("A post cannot be empty!")
            return redirect(url_for('forum.home'))
        post = ForumPost(
            title=request.form['title'],
            author=current_user.email,
            tags=(json.dumps(get_tags(request.form['tags'])) if is_tag_str(request.form['tags']) else ''),
            post=request.form['post'],
            posts=0,
            views=0,
            created=datetime.utcnow(),
            last_edited=datetime.utcnow(),
            reply_to=None
        )
        db.session.add(post)
        friends = get_friends(current_user.email)
        for friend in friends:
            notification = Notification(
                user_email=friend.email,
                description=current_user.username + " made a new forum post: " + post.title,
                link=url_for('forum.view', post_id=post.id)
            )
            db.session.add(notification)
        db.session.commit()
        return redirect(url_for('forum.home'))

@forum.route('/<post_id>/view', methods=['GET', 'POST'])
@login_required
def view(post_id):
    # Get post
    post = ForumPost.query.filter(ForumPost.id == post_id).first()
    user = User.query.filter(User.email == post.author).first().username

    if request.method == 'POST':
        if not request.form['post']:
            flash("A reply cannot be empty!")
        else:
            # Add the reply
            reply = ForumPost(
                title='',
                author=current_user.email,
                tags='[]',
                post=request.form['post'],
                posts=0,
                views=0,
                created=datetime.utcnow(),
                last_edited=datetime.utcnow(),
                reply_to=int(request.form['replyto'])
            )
            db.session.add(reply)

            # Increment number of replies
            post.posts = post.posts + 1
            post.last_edited = datetime.utcnow()

            # Commit changes to db
            db.session.commit()

    # Increment views
    post.views = post.views + 1
    db.session.commit()

    # Load post data
    data = {}
    data['id'] = post.id
    data['title'] = post.title
    data['user'] = user
    data['created'] = post.created.strftime(time_format)
    data['tags'] = json.loads(post.tags)
    data['data'] = post.post
    data['posts'] = post.posts
    data['views'] = post.views
    data['activity'] = post.last_edited.strftime(time_format)
    return render_template('forum/view.html', post=data, replies=get_replies(post_id))

def get_replies(post_id):
    replies = []
    data = ForumPost.query.filter(ForumPost.reply_to == post_id).all()
    for entry in data:
        reply = {}
        reply['id'] = entry.id
        reply['user'] = User.query.filter(User.email == entry.author).first().username
        reply['content'] = entry.post
        reply['created'] = entry.created.strftime(time_format)
        reply['replies'] = get_replies(entry.id)
        replies.append(reply)
    
    return replies