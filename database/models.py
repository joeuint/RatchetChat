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

class ConvoConnection(Base):
    __tablename__ = 'convo_connections'
    connection_id = Column(String, nullable=False, primary_key=True)
    user1 = Column(String, ForeignKey('users.user_id'), nullable=False)
    user2 = Column(String, ForeignKey('users.user_id'), nullable=False)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True, nullable=False)
    connection_id = Column(String, ForeignKey('convo_connections.connection_id'))
    content = Column(String, nullable=False)
