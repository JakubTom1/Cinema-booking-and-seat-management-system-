from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

# Connection to MySQL database
url_address = "mysql+pymysql://szewcza1:rswiw3r376trLrTi@mysql.agh.edu.pl:3306/szewcza1"
engine = create_engine(url_address)
Base = declarative_base()
metadata = MetaData()
def init_db():
    Base.metadata.create_all(engine)
