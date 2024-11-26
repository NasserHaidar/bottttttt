from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database setup
engine = create_engine("sqlite:///bot_database.db")  # SQLite database
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if not already present
Base.metadata.create_all(engine)
