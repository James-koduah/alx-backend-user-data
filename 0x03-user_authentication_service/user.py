#!/usr/bin/env python3
"""user class model"""
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Text, ForeignKey, Boolean
from datetime import datetime
import uuid
import bcrypt


Base = declarative_base()


class User(Base):
    """orm representation of a user"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)
