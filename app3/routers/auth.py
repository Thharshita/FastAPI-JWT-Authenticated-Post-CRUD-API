from fastapi import APIRouter, status,HTTPException,Depends,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app3 import database,schemas,models,utils,oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token)
# def login (user_credential: schemas.UserLogin,db:Session=Depends(database.get_db)): By using OAuth2PasswordRequestForm, you're explicitly indicating that your route is intended for OAuth 2.0 password grant requests. This makes the purpose of the route clearer to anyone reading the code.
def login (user_credential: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)): 
    user=db.query(models.User).filter(models.User.email == user_credential.username).first()  #user_credential.email == user_credential.username
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credential.password, user.password):  #models.User.id
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token =oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}

    













# By specifying user_credential: OAuth2PasswordRequestForm = Depends() in your FastAPI route,
# you're telling FastAPI to automatically parse the incoming request body and extract the form data, such as the username and password, into an instance of
# OAuth2PasswordRequestForm. This allows you to conveniently access the form data in your route handler function without needing to manually parse it yourself.