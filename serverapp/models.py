from .database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = 'users'
    user_id         = Column(String, primary_key=True, nullable=False)
    hashed_password = Column(String, nullable=False)

