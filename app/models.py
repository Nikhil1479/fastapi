from sqlalchemy import create_engine, Column, Integer, String, Boolean, CHAR
from .database import Base
from .database import SessionLocal
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('True'))
    created_At = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
