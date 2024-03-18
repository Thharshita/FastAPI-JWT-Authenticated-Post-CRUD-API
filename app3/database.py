#sqlalchemy doesnt know how to talk to the database, it has all the code to write query in python and define all the models , hence database drievr psycopg is installed


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
                #postgresql://,username:,password.@localhost:5432/,database.
SQL_DATABASE_URL='postgresql://postgres:alone@localhost:5432/fastapi'

engine=create_engine(SQL_DATABASE_URL) #resposible to connect alchemy to databae

#if u actually want to talk to database u use session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency  
#sessionlocal obj is responsible to talking to db
#we create a function where we actually get connected to our database or get a session to to database
#we just keep calling this function everytime we send request to our api
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
#all the models that we r going to define to create out table in postgres is going to extend this class