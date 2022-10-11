from sqlalchemy import Column, Text, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, unique=True, index=True)
    name = Column(String(255))
    image_filename = Column(String(255))
    thumb = Column(String(255))
