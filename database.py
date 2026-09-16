from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()


engine = create_engine(os.getenv('DATABASE_URL'))
session_local = sessionmaker(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

