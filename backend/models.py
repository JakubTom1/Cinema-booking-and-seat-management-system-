from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
#from database import Base, engine

# kwestie technicze to będzie do usunięcia
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

# Connection to MySQL database
url_address = "mysql+pymysql://szewcza1:rswiw3r376trLrTi@mysql.agh.edu.pl:3306/szewcza1"
engine = create_engine(url_address)
Base = declarative_base()
metadata = MetaData()
# dotąd

# Model of Clients
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(15), index=True)
    last_name = Column(String(15), index=True)
    status = Column(Integer, index=True) # client(2), cinema staff(1) or admin(0)
    login = Column(String(15), unique=True, index=True)
    password = Column(String(15), unique=True, index=True)

    transactions = relationship("Transaction", back_populates="user")

# Model of Movies
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String(50), index=True)

    showings = relationship("Showing", back_populates="movie")

# Model of Showing
class Showing(Base):
    __tablename__ = 'showings'

    id = Column(Integer, primary_key=True, index=True)
    id_movies = Column(Integer, ForeignKey('movies.id'))
    date = Column(Date)
    hour = Column(Time)
    id_hall = Column(Integer, ForeignKey('halls.id'))

    movie = relationship("Movie", back_populates="showing")
    hall = relationship("Hall", back_populates="showing")

# Model of Screening room
class Hall(Base):
    __tablename__ = 'halls'

    id = Column(Integer, primary_key=True, index=True)
    hall_num = Column(Integer, index=True)
    seats_amount = Column(Integer, index=True)
    free_seats = Column(Integer, index=True)

    showings = relationship("Showing", back_populates="hall")
    seats = relationship("Seat", back_populates="hall")

# Model of Transaction
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    id_users = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric(10, 2))
    status = Column(String(15), index=True)
    date = Column(Date)

    user = relationship("User", back_populates="transactions")

# Model of Places
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    id_halls = Column(Integer, ForeignKey('halls.id'))
    seat_num = Column(Integer, index=True)
    row = Column(Integer, index=True)
    occupied = Column(Boolean, default=True)

    hall = relationship("Hall", back_populates="seats")

# Gate between tables Transactions and Sits
class Gate(Base):
    __tablename__ = 'gate'
    id = Column(Integer, primary_key=True, index=True)
    id_seats = Column(Integer, ForeignKey('seats.id'))
    id_transaction = Column(Integer, ForeignKey('transactions.id'))

    seat = relationship("Seat", back_populates="gate")
    transaction = relationship("Transaction", back_populates="gate")

Base.metadata.create_all(engine)