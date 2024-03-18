from app3 import models
from app3 import schemas
from app3 import utils
from app3.database import get_db
from fastapi import FastAPI, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session


#CREATE USER 
router= APIRouter(prefix="/users",tags=["Users"])
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db :Session=Depends(get_db)):
    #hash the password
    hashed_password=utils.hash_pass(user.password)
    user.password=hashed_password
    new_user =models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get the user data

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session= Depends(get_db)):
    post= db.query(models.User).filter(models.User.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with id :{id}")
    return post