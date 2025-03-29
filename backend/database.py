from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Łączenie z bazą danych SQLite (możesz dostosować do innego DB)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Tworzymy engine do połączenia z bazą
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Bazowa klasa dla modeli
Base = declarative_base()

# Tworzymy sesję do komunikacji z DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funkcja, która tworzy tabele w bazie
def init_db():
    Base.metadata.create_all(bind=engine)
