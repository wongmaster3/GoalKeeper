from conftest import handler
# from conftest import Session, User

testing = True

def test_logout():
    if testing:
        # For in docker container tests
        # Initilize the app and client
        h = handler
        # h = TestHandler()
        app = h.app
        client = h.client

        # register and login new user
        h.register("d", "d@gmail.com", "d")
        response = client.post("/accounts/login", data={"email": "d@gmail.com", "password": "d"})

        # Check we are on the home page
        assert "http://localhost/accounts/home" == response.headers["Location"]

        # Logout of account and check status code
        assert client.get("/accounts/logout").status_code == 200

        # Remove the user
        h.remove_user("d@gmail.com")
    else:
        assert 1 == 2
        # # For ci/cd pipeline
        # session = Session()
        # user = User(username='a', email='a@gmail.com', password='a')
        # session.add(user)
        # # session.commit()
        # assert user is not None