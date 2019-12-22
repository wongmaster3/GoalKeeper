from conftest import handler
from goalkeeper.models import Goal

testing = True;

def test_goal():
    if testing:
        # Initilize the app and client
        h = handler
        # h = TestHandler()
        app = h.app
        client = h.client

        # register and login new user
        h.register("z", "z@gmail.com", "z")
        client.post("/accounts/login", data={"email": "z@gmail.com", "password": "z"})

        # Check we are on the add_goals page
        assert client.get("/goals/add_goal").status_code == 200

        # Add a goal and check that it succeeds
        response = client.post("/goals/add_goal", data={"title": "test", "description": "test"})

        assert "http://localhost/accounts/home" == response.headers["Location"]

        # Check database that goal was added
        with app.app_context():
            assert (
                    Goal.query.filter(Goal.user_email == "z@gmail.com").first()
                    is not None
            )

        # Remove the user
        h.remove_goals("z@gmail.com")
        h.remove_user("z@gmail.com")
    else:
        assert 1 == None
        # from conftest import Session, Goal
        # session = Session()
        # goal = Goal(user_email='b', title='b@gmail.com', description='b')
        # session.add(goal)
        # # session.commit()
        # assert goal is not None