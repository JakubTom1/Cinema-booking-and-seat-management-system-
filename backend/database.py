from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection to SQLite database (---edit---)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Make engine of database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Base class of model
Base = declarative_base()

# Make session of communication with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database initialization
def init_db():
    Base.metadata.create_all(bind=engine)
