from flask_nav.elements import Navbar, View, Separator
from goalkeeper import nav
from flask_login import current_user

@nav.navigation()
def account_nav():
        return Navbar(
            'GoalKeeper',
            View('Home', 'accounts.home'),
            View('Feed', 'feed.home'),
            View('Create Goal', 'goals.add_goal'),
            View('Completed Goals', 'accounts.completed_goals' ),
            View('Calendar', 'accounts.view_calendar'),
            View('Find Friends', 'friends.list_friends'),
            View('Forums', 'forum.home'),
            View('Logout', 'accounts.logout'),
        )
