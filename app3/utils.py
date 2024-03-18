from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #we are telling pathlib what is the default algorithm, we want to use bcrypt hashing algorithm


def hash_pass(passwd:str):
    return pwd_context.hash(passwd)


def verify(plain_passwd, hash_pass):
    return pwd_context.verify(plain_passwd, hash_pass)
