
import os
import random
import string

from sqlalchemy import Column, Integer, String, Boolean


def init_models(db):

    class User(db.model):
        __tablename__ = 'users'
        id = Column('id', String(10), primary_key=True)
        email = Column('email', String)
        user_id = Column('user_id', Integer)
        user_name = Column('user_name', String)
        first_name = Column('first_name', String)
        last_name = Column('last_name', String)
        level = Column('level', String, default='user')
        enabled = Column('enabled', Boolean, default=True)

        def __init__(self, email, **kwargs):
            self.email = email
            self.id = self.generate_id()
            for attr, value in kwargs.items():
                if value in ["None", None]: continue
                setattr(self, attr, value)

        def __repr__(self):
            return "<User('%s','%s', '%s')>" % (self.id, self.user_name, self.email)

        def generate_id(self, length=10):
            return ''.join(random.choice(string.ascii_letters) for _ in range(length))

        @staticmethod
        def add(user_id, email, **kwargs):
            user = db.session.query(User).filter(User.user_id == user_id).first()
            if user is not None:
                user.email = email
                for attr, value in kwargs.items():
                    if value in ["None", None]: continue
                    setattr(user, attr, value)
            else:
                user = User(email, user_id=user_id, **kwargs)
            db.session.add(user)
            return user.id

        @staticmethod
        def enable(id, value):
            user = db.session.query(User).filter(User.id == id).first()
            if user:
                user.enabled = value
                db.session.add(user)
            return user

        @staticmethod
        def is_added(user_id):
            user = db.session.query(User).filter(
                User.user_id == user_id
            ).first()
            return user is not None

        @staticmethod
        def is_logged(user_id):
            user = db.session.query(User).filter(
                User.user_id == user_id,
                User.enabled == True
            ).first()
            return user is not None

        @staticmethod
        def is_admin(user_id):
            user = db.session.query(User).filter(
                User.user_id == user_id,
                User.enabled == True,
                User.level == 'admin'
            ).first()
            return user is not None

        @staticmethod
        def login(id, **kwargs):
            user = db.session.query(User).filter(
                User.id == id,
                User.user_id == None
            ).first()
            if user is None: return False
            for attr, value in kwargs.items():
                if hasattr(user, attr): setattr(user, attr, value)
            user.enabled = True
            db.session.add(user)
            return True

        @staticmethod
        def logout(user_id):
            user = db.session.query(User).filter(
                User.user_id == user_id,
                User.enabled == True
            ).first()
            if user is None: return False
            user.enabled = False
            db.session.add(user)
            return True

        @staticmethod
        def query(**kwargs):
            return db.session.query(User).filter_by(**kwargs).all()


    db.User = User
