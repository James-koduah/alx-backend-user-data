#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates and saves a user object to the database"""
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, *args, **kwargs) -> User:
        """Query the database for a user filtered by attributes"""
        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound

    def update_user(self, user_id, *args, **kwargs) -> None:
        """Update a user based on thier id"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError

        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
