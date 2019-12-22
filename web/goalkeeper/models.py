import flask_sqlalchemy
import datetime

db = flask_sqlalchemy.SQLAlchemy()

##### The Tables for the Database ######

# User Table
class User(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

# Goals Table
class Goal(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String, default="", nullable=False)
    completion = db.Column(db.Boolean, default=False, nullable=False)
    private_goal = db.Column(db.Boolean, nullable=False)

# Friends Table
class Friend(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_email = db.Column(db.String(100), nullable=False)
    user2_email = db.Column(db.String(100), nullable=False)

# Notifications Table
class Notification(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    clicked = db.Column(db.Boolean, default=False, nullable=False)
    link = db.Column(db.String(500), nullable=True)

# List of all used tags
class Tag(db.Model):
    text = db.Column(db.String(100), nullable=False, primary_key=True)

# Forum posts
class ForumPost(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    tags = db.Column(db.Text, default="", nullable=False)
    post = db.Column(db.Text, nullable=False)
    posts = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    reply_to = db.Column(db.Integer)

# Feed Table for when friends are added, when goals are added by friends,
# and when goals are completed by friends.
class Feed(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#convenience functions for common database tasks
def get_pending_sent(email):
    friend_query1 = Friend.query.filter(Friend.user1_email == email).with_entities(Friend.user2_email.label('user1_email'))
    friend_query2 = Friend.query.filter(Friend.user2_email == email).with_entities(Friend.user1_email)
    intersection = friend_query1.intersect(friend_query2)
    pending_set_sent = friend_query1.except_(intersection)
    return User.query.filter(User.email.in_(pending_set_sent))

def get_pending_received(email):
    friend_query1 = Friend.query.filter(Friend.user1_email == email).with_entities(Friend.user2_email.label('user1_email'))
    friend_query2 = Friend.query.filter(Friend.user2_email == email).with_entities(Friend.user1_email)
    intersection = friend_query1.intersect(friend_query2)
    pending_set_receive = friend_query2.except_(intersection)
    return User.query.filter(User.email.in_(pending_set_receive))

def get_friends(email):
    friend_query1 = Friend.query.filter(Friend.user1_email == email).with_entities(Friend.user2_email.label('user1_email'))
    friend_query2 = Friend.query.filter(Friend.user2_email == email).with_entities(Friend.user1_email)
    intersection = friend_query1.intersect(friend_query2)
    friends_of_user = User.query.filter(User.email.in_(intersection))
    return friends_of_user
