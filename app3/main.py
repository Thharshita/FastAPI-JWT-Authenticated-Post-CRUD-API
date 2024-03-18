#I have not deleted the psycopg2 path operation so that u can compare the path operation

from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
from app3 import models  # Importing models.py directly
from app3 import schemas # Importing schemas.py directly
from app3 import utils # Importing utils.py directly
from app3.database import  engine,get_db
from sqlalchemy.orm import Session
from app3.routers import post, user,auth

models.Base.metadata.create_all(bind=engine)


# whe we run api , db:Session=Depends(get_db) going to give access to db,it will create a session to our database and perform operation then close it
app=FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

