from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from database import Base

# Model Klientów
class Klient(Base):
    __tablename__ = 'klienci'

    id = Column(Integer, primary_key=True, index=True)
    imie = Column(String, index=True)
    nazwisko = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    haslo = Column(String)

    transakcje = relationship("Transakcja", back_populates="klient")

# Model Filmów
class Film(Base):
    __tablename__ = 'filmy'

    id = Column(Integer, primary_key=True, index=True)
    tytul = Column(String, index=True)
    grany_od = Column(Date)
    grany_do = Column(Date)

    seanse = relationship("Seans", back_populates="film")

# Model Seansów
class Seans(Base):
    __tablename__ = 'seanse'

    id = Column(Integer, primary_key=True, index=True)
    id_film = Column(Integer, ForeignKey('filmy.id'))
    data = Column(Date)
    godzina = Column(Time)
    id_sala = Column(Integer, ForeignKey('sale.id'))

    film = relationship("Film", back_populates="seanse")
    sala = relationship("Sala", back_populates="seanse")

# Model Sal
class Sala(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True, index=True)
    liczba_miejsc = Column(Integer)
    liczba_wolnych_miejsc = Column(Integer)

    seanse = relationship("Seans", back_populates="sala")
    miejsca = relationship("Miejsce", back_populates="sala")

# Model Transakcji
class Transakcja(Base):
    __tablename__ = 'transakcje'

    id = Column(Integer, primary_key=True, index=True)
    id_klienta = Column(Integer, ForeignKey('klienci.id'))
    kwota = Column(Numeric(10, 2))
    status = Column(String)
    data = Column(Date)

    klient = relationship("Klient", back_populates="transakcje")

# Model Miejsc
class Miejsce(Base):
    __tablename__ = 'miejsca'

    id = Column(Integer, primary_key=True, index=True)
    numer_miejsca = Column(Integer)
    czy_wolne = Column(Boolean, default=True)
    id_sali = Column(Integer, ForeignKey('sale.id'))

    sala = relationship("Sala", back_populates="miejsca")
