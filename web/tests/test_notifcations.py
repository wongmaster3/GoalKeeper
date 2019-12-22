from conftest import handler
from goalkeeper.models import Goal, Notification


def test_notifications():

    # Initilize the app and client
    h = handler
    # h = TestHandler()
    app = h.app
    client = h.client

    # register and login new user
    h.register("f", "f@gmail.com", "f")
    client.post("/accounts/login", data={"email": "f@gmail.com", "password": "f"})
    # logout new user
    assert client.get("/accounts/logout").status_code == 200

    h.register("g", "g@gmail.com", "g")
    client.post("/accounts/login", data={"email": "g@gmail.com", "password": "g"})

    assert client.get("/friends/add_friend/f@gmail.com").status_code == 302
    client.get("/accounts/logout")

    # Log in once again with f@gmail.com
    client.post("/accounts/login", data={"email": "f@gmail.com", "password": "f"})

    # Accept Friend Request from g@gmail.com
    assert client.get("/friends/add_friend/g@gmail.com").status_code == 302

    response = client.post("/goals/add_goal", data={"title": "test", "description": "test"})

    with app.app_context():
        assert (
            Notification.query.filter(Notification.user_email == "f@gmail.com").all()
            is not None
        )
    h.remove_friend("g@gmail.com")
    h.remove_friend("f@gmail.com")
    h.remove_user("f@gmail.com")
    h.remove_user("g@gmail.com")
    Notification.query.filter(Notification.user_email == "g@gmail.com").delete()
    Notification.query.filter(Notification.user_email == "f@gmail.com").delete()
