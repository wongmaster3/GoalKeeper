import os
import tempfile

import pytest
import goalkeeper
from goalkeeper.models import db
from goalkeeper.models import User, Goal, Friend
from goalkeeper import create_app

class TestHandler():
    app = None
    client = None

    def __init__(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False

    def register(self, username, email, password):
        return self.client.post("/accounts/register",
                                data={"username":username, "email":email, "password":password})

    def login(self, username, password):
        return self.client.post(
            "/accounts/login", data={"username": username, "password": password}
        )

    def remove_user(self, temp):
        User.query.filter(User.email == temp).delete()
        db.session.commit()

    def remove_goals(self, temp):
        Goal.query.filter(Goal.user_email == temp).delete()
        db.session.commit()

    def remove_friend(self, temp):
        Friend.query.filter(Friend.user1_email == temp).delete()
        db.session.commit()


handler = TestHandler()


# CI/CD Pipeline Testing
# from sqlalchemy import create_engine
# engine = create_engine('postgres:///:memory:', echo=True)
#
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
#
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
#
# from sqlalchemy import Column, Integer, String
# class User(Base):
#     __tablename__ = 'users'
#     # id = db.Column(db.Integer, autoincrement=True)
#     username = Column(String, nullable=False)
#     email = Column(String, primary_key=True)
#     password = Column(String, nullable=False)
#
# class Goal(Base):
#     __tablename__ = 'goals'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     user_email = Column(String(100), nullable=False)
#     title = Column(String(100), nullable=False)
#     description = Column(String(100), nullable=False)