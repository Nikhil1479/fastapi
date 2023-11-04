from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, CHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import models


SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:niks1479@localhost/fastapi"

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    age = Column("age", Integer)
    gender = Column("gender", CHAR)

    def __init__(self, ssn, firstname, lastname, age, gender):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"Person(ssn={self.ssn}, firstname={self.firstname}, lastname={self.lastname}, age={self.age}, gender={self.gender})"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()

p1 = Person(2, "Nikhil", "Gupta", 25, "M")
session.add(p1)

p2 = Person(3, "Manas","Gupta", 21, "M")
session.add(p2)

p3 = Person(4, "Deepa","Gupta",18,"F")
session.add(p3)

session.commit()

print(p1)