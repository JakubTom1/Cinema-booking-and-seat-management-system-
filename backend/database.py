"""
Moduł odpowiedzialny za konfigurację bazy danych i zarządzanie sesjami.
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator


# Tworzenie połączenia z bazą danych MySQL
url_address = "mysql+pymysql://szewcza1:rswiw3r376trLrTi@mysql.agh.edu.pl:3306/szewcza1"
engine = create_engine(url_address)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

def init_db():
    """
    Inicjalizacja bazy danych, tworząc wszystkie tabele na podstawie modeli SQLAlchemy
    """
    Base.metadata.create_all(engine)

def get_db() -> Generator:
    """
    Generator zarządzający sesją bazy danych. Otwiera sesję, a po zakończeniu zamyka ją.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
