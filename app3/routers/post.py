from app3 import models
from app3 import oauth2
from app3 import schemas
from typing import List
from app3.database import  get_db
from fastapi import FastAPI, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session


router= APIRouter(prefix="/posts",tags=["POST"])
# try:
#     conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="alone",cursor_factory=RealDictCursor)
#     cursor=conn.cursor()
#     print("Database Connection is successfull")

# except Exception as error:
#     print("Connecting to Database failed")
#     print("Error",error)


@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    posts= db.query(models.Post).all()   #models.Post allow us access the model to make query to our posts tabel
    # print(posts) #after removing .all(), u will see the sql query here
    # return {"data":posts} 

    return posts  #automatic convert it to json 

# @app.get("/posts")
# def get_posts():
#     cursor.execute("Select * from posts")
#     post= cursor.fetchall()
#     print(post)
#     return {"data":post} 



#nytime nyone want to access resource that requires logged in , we going to expect them to provide the access token.
#Create
#if u want the endpint to be protect that only logined user should be allowed to make post requests
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostBase,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):    #Depends(oauth2.get_current_user) this depedency will call get_current_user function
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #what if we have more feild , itis not reliable to write all columns andit values hence
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return {"data":new_post} 
    return new_post

# @app.post("/posts")
# def create_post(post:Post):  
#     #cursor.execute(f"Insert into posts (title,content,published) Values ({post.title},{post.content},{post.published}")  #is vulnerable to SQL Injection, hence not use this.
#     cursor.execute("""Insert into posts (title,content,published) Values (%s,%s,%s) Returning *""",(post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}


    
#READ

@router.get("/{id}")  
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):  
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not found")
    # return {"post_detail":post}  
    return post

# @app.get("/posts/{id}")  
# def get_post(id:int):  
#     cursor.execute("""Select * from posts where id=%s""", (str(id),))
#     fetch=cursor.fetchone() 
#     if not fetch:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not found")
#     return {"post_detail":fetch}  




#DELETE

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)  #will delete all post that contain id
   # post is a SQLAlchemy query object. Even if no rows match the query condition, post_query itself won't be None. It will always be a valid query object.
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} does not exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()


# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""Delete from posts where id=%s returning *""",(str(id)))
#     delete_it= cursor.fetchone()
#     conn.commit()
#     if delete_it==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



#UPDATE
@router.put('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(updated_post:schemas.PostBase,id: int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id)
    post_first=post.first()
    if post_first==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} does not exist")
    if post_first.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform this action")
    
    post.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post.first()

# @app.put('/posts/{id}')
# def update_post(id:int,post:Post):
#     cursor.execute("""Update posts set title=%s,content=%s,published=%s where id=%sreturning*""",(post.title,post.content,post.published,str(id)))
#     update_it= cursor.fetchone()
#     conn.commit()
#     if  update_it== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{id} does not exist")
#     return {"data":update_it}




