from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from app3 import schemas,database,models
from fastapi import Depends, HTTPException,status,Depends
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
#Secret key   #reside on the servee that handles data integrity
#Algorith
#expriation time
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    print("Token Before Encoding:", to_encode)
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print("Encoded Token:", encoded_jwt)
    return encoded_jwt



def verify_access_token(token:str,credentials_exception):
    try:
        print("Token to Decode:", token)
        payload=jwt.decode(token,SECRET_KEY,[ALGORITHM])   #. Upon decoding, you can retrieve the payload, which contains the user information.
        print("Decoded Payload:", payload)
        id=payload.get("user_id") #After decoding, you obtain the payload, which contains information about the user. You can use the get() function to retrieve specific information from the payload, such as the user ID.
        print("User ID:", id)
        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id) 
    except JWTError as e:
        print("JWTError:", e)
        raise credentials_exception
    return token_data   #sends the user data 
    

#when user logged in using token we pass it to get_current_user which then verify the token, and wehn token is valid then will return token data
def get_current_user(token:str= Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)  #token have user data
    user =db.query(models.User).filter(models.User.id==token.id).first()  #user has entire post of that user like entire row of db.
    return user