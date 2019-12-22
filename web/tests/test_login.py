from conftest import handler

testing = True;

def test_register():
    if testing:
        # Initilize the app and client
        h = handler
        # h = TestHandler()
        app = h.app
        client = h.client

        assert client.get("/accounts/login").status_code == 200

        # test that login redirects to the home page
        h.register("b", "b@gmail.com", "b")
        response = client.post("/accounts/login", data={"email": "b@gmail.com", "password": "b"})
        assert "http://localhost/accounts/home" == response.headers["Location"]

        # Remove the user
        h.remove_user("b@gmail.com")
    else:
        assert 1 == 2
        # # For ci/cd pipeline
        # from conftest import Session, User
        # session = Session()
        # user = User(username='a', email='a@gmail.com', password='a')
        # session.add(user)
        # # session.commit()
        # assert user is not None