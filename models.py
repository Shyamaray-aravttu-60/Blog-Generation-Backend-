from sqlalchemy import Integer , String , Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String , nullable=False , unique=True)
    password= Column(String)