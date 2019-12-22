from flask import Flask, render_template, flash
from goalkeeper.accounts.forms import LoginForm
from flask_login import LoginManager
from flask_nav import Nav

from goalkeeper.models import db, User
from . import config

login_manager = LoginManager()
nav = Nav()
app = Flask(__name__)

def create_app(test_config=None):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super secret key'

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.update(test_config)

    app.app_context().push()
    db.init_app(app)

    # Register the blueprints
    from goalkeeper.accounts.routes import accounts
    from goalkeeper.goals.routes import goals
    from goalkeeper.friends.routes import friends
    from goalkeeper.notifications.routes import notifications
    from goalkeeper.forum.routes import forum
    from goalkeeper.feed.routes import feed

    app.register_blueprint(accounts)
    app.register_blueprint(goals)
    app.register_blueprint(friends)
    app.register_blueprint(notifications)
    app.register_blueprint(forum)
    app.register_blueprint(feed)

    # Initialize the user loader
    @login_manager.user_loader
    def load_user(user_id):
        #flash(user_id)
        return User.query.get(user_id)

    # Initialize login manager
    login_manager.login_view = 'accounts.login'
    login_manager.init_app(app)

    # Initialize the navigation bar
    from goalkeeper.navigation import account_nav
    nav.init_app(app)

    # Login page will be the home page
    @app.route('/')
    def index():
        form = LoginForm()
        return render_template("login.html", form=form)

    return app

if __name__ == "__main__":
    app.run(threaded=True)

