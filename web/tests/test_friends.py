from conftest import handler
from goalkeeper.models import Friend

def test_friends():
    # Initilize the app and client
    h = handler
    # h = TestHandler()
    app = h.app
    client = h.client

    # register and login new user
    h.register("e", "e@gmail.com", "e")
    client.post("/accounts/login", data={"email": "e@gmail.com", "password": "e"})

    # Check we are on the list_friends page
    assert client.get("/friends/list_friends").status_code == 200

    # Check database that user has no friends
    with app.app_context():
        assert (
                Friend.query.filter(Friend.user1_email == "e@gmail.com").first()
                is None
        )
        assert (
                Friend.query.filter(Friend.user2_email == "e@gmail.com").first()
                is None
        )

    # Remove the user
    h.remove_user("e@gmail.com")

# Test that adding one friend results in a pending relationship
def test_add_friends_pending():
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

    # Check database that user has someone they can add
    with app.app_context():
        assert (
                Friend.query.filter(Friend.user1_email == "g@gmail.com").first()
                is not None
        )
        assert (
                Friend.query.filter(Friend.user2_email == "f@gmail.com").first()
                is not None
        )

    # Remove the user
    h.remove_friend("g@gmail.com")
    h.remove_user("f@gmail.com")
    h.remove_user("g@gmail.com")

# Test that adding friends results in two way relationship
def test_add_friends_final():
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

    # Check database that user has someone they can add
    with app.app_context():
        # There is a two way relationship between 'g' and 'f'
        assert (
                Friend.query.filter(Friend.user1_email == "g@gmail.com").first()
                is not None
        )
        assert (
                Friend.query.filter(Friend.user2_email == "f@gmail.com").first()
                is not None
        )
        assert (
                Friend.query.filter(Friend.user1_email == "f@gmail.com").first()
                is not None
        )
        assert (
                Friend.query.filter(Friend.user2_email == "g@gmail.com").first()
                is not None
        )

    # Remove the user
    h.remove_friend("g@gmail.com")
    h.remove_friend("f@gmail.com")
    h.remove_user("f@gmail.com")
    h.remove_user("g@gmail.com")