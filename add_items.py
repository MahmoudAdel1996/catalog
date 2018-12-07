from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

engine = create_engine('sqlite:///products.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
