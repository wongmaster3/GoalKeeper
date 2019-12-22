from goalkeeper.models import User
from conftest import handler

testing = True

def test_register():
    if testing:
        # For docker container tests
        # Initilize the app and client
        h = handler
        # h = TestHandler()
        app = h.app
        client = h.client

        assert client.get("/accounts/register").status_code == 200

        # test that successful registration redirects to the login page
        response = client.post("/accounts/register", data={"username":"a", "email":"a@gmail.com", "password":"a"})
        assert response.status_code == 200

        # test that the user was inserted into the database
        with app.app_context():
            assert (
                User.query.filter(User.email == "a@gmail.com").first()
                is not None
            )

        # Remove the user
        h.remove_user("a@gmail.com")
    else:
        assert 1 == 2
        # # For ci/cd pipeline
        # from conftest import Session, User
        # session = Session()
        # user = User(username='a', email='a@gmail.com', password='a')
        # session.add(user)
        # # session.commit()
        # assert user is not None