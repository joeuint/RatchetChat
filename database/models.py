from .database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    user_id         = Column(String, primary_key=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class ConvoRequest(Base):
    __tablename__ = 'convo_requests'
    convo_request_id = Column(String, primary_key=True, nullable=False)
    requester_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    target_id = Column(String, ForeignKey('users.user_id'), nullable=False)