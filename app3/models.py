#create table in the database

from app2.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):   #base from sqlalchemy #this class name only python knows
    __tablename__ = 'posts' 

    id=Column(Integer, primary_key=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable =False)
    published=Column(Boolean, nullable =False,server_default="True")
    created_at=Column(TIMESTAMP(timezone=True),
                    nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),nullable=False)


#This is the SQLAlchemy User model, which represents the structure of your database table.
#This model expects keyword arguments corresponding to the columns defined in the table schema.

class User(Base):
    __tablename__ = 'users'
    id=Column(Integer, nullable=False,primary_key=True)
    email=Column(String, nullable=False,unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))