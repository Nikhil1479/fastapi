from sqlalchemy import create_engine, Column, Integer, String, Boolean, CHAR
from database import Base
from database import SessionLocal

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)