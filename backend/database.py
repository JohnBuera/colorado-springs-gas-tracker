# Importing the function that creates the connnection interface 
from sqlalchemy import create_engine

# session maker creates database sessions 
# delcarative_base will be sed to create the base class that our model classes will inherit from
from sqlalchemy.orm import sessionmaker, declarative_base

# This string will tell SQLAlchemy: 
# What database system is being used (PosterSQL)
# What use5rname to use 
# What password to use 
# What database is called 
# FREEDOM is the password (AOT Reference) >:3

DATABASE_URL = "sqlite:///./gas_tracker.db"

# Creating teh SQLAlchemy engine 
engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False})





# Create a factor for database sessions 
SessionLocal = sessionmaker(
    autocommit=False,   
    autoflush=False,
    bind=engine
)

# Creating a base class that our database models will inherit from 
Base = declarative_base()
