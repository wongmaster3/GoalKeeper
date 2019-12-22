from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from goalkeeper import app
from goalkeeper.models import db
from datetime import datetime

from goalkeeper.models import User, ForumPost
from datetime import datetime

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    test_user = User(
        username="test",
        email="test@test.com",
        password=generate_password_hash("test")
    )
    db.session.add(test_user)
    db.session.commit()

    test_post = ForumPost(
        title="Test Post Title",
        author="test@test.com",
        tags='["#Test tag 1", "#Test tag 2"]',
        post="This is a test post text area",
        posts=4,
        views=4123,
        created=datetime.utcnow(),
        last_edited=datetime.utcnow(),
        reply_to=None
    )
    db.session.add(test_post)
    db.session.commit()

    reply1 = ForumPost(
        title="",
        author="test@test.com",
        tags='[]',
        post="This is reply",
        posts=0,
        views=0,
        created=datetime.utcnow(),
        last_edited=datetime.utcnow(),
        reply_to=1
    )
    db.session.add(reply1)
    db.session.commit()

    reply2 = ForumPost(
        title="",
        author="test@test.com",
        tags='[]',
        post="This is reply to the first reply",
        posts=0,
        views=0,
        created=datetime.utcnow(),
        last_edited=datetime.utcnow(),
        reply_to=2
    )
    db.session.add(reply2)
    db.session.commit()

    reply3 = ForumPost(
        title="",
        author="test@test.com",
        tags='[]',
        post="This is reply to a reply to the first reply",
        posts=0,
        views=0,
        created=datetime.utcnow(),
        last_edited=datetime.utcnow(),
        reply_to=3
    )
    db.session.add(reply3)
    db.session.commit()

    reply4 = ForumPost(
        title="",
        author="test@test.com",
        tags='[]',
        post="This is a second reply",
        posts=0,
        views=0,
        created=datetime.utcnow(),
        last_edited=datetime.utcnow(),
        reply_to=1
    )
    db.session.add(reply4)
    db.session.commit()


if __name__ == "__main__":
    cli()