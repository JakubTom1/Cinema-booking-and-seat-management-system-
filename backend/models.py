import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))


from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship, backref
from database import Base

# Model of Clients
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(15), index=True)
    last_name = Column(String(15), index=True)
    status = Column(String(15), unique=True, index=True) # client, cinema staff or admin
    login = Column(String(15), unique=True, index=True)
    password = Column(String(15), unique=True, index=True)

# Model of Movies
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String(50), index=True)

# Model of Showing
class Showing(Base):
    __tablename__ = 'showings'

    id = Column(Integer, primary_key=True, index=True)
    id_movies = Column(Integer, ForeignKey('movies.id'))
    date = Column(Date)
    hour = Column(Time)
    id_hall = Column(Integer, ForeignKey('halls.id'))

    movie = relationship("Movie", backref=backref("showings", cascade="all, delete-orphan"))
    hall = relationship("Hall", backref=backref("showings", uselist=False))
# Model of Screening room
class Hall(Base):
    __tablename__ = 'halls'

    id = Column(Integer, primary_key=True, index=True)
    hall_num = Column(Integer, index=True)
    seats_amount = Column(Integer, index=True)
    free_seats = Column(Integer, index=True)

# Model of Transaction
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    id_users = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric(10, 2))
    status = Column(String(15), index=True)
    date = Column(Date)

    user = relationship("User", backref=backref("transactions"))

# Model of Places
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    id_halls = Column(Integer, ForeignKey('halls.id'))
    seat_num = Column(Integer, index=True)
    row = Column(Integer, index=True)
    occupied = Column(Boolean, default=True)

    hall = relationship("Hall", backref=backref("seats"))
    gate = relationship("Gate", backref=backref("seats", uselist=False))

# Gate between tables Transactions and Sits
class Gate(Base):
    __tablename__ = 'gate'
    id = Column(Integer, primary_key=True, index=True)
    id_seats = Column(Integer, ForeignKey('seats.id'))
    id_transaction = Column(Integer, ForeignKey('transactions.id'))

    transaction = relationship("Transaction", backref=backref("gate"))