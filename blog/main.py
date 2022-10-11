from typing import List
from fastapi import FastAPI, Depends, status, HTTPException

from blog.hashing import Hash
from . import schemas,models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()

@app.post('/', status_code=status.HTTP_201_CREATED,tags=['blog'])
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title,body=req.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
def delete_blog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Blog is Deleted'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id- {id} is not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'

@app.get('/blog', response_model=List[schemas.ShowBlog],tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=['blog'])
def show(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id - {id} is not found')
    return blog



@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(req: schemas.User,db: Session = Depends(get_db)):
    new_user =  models.User(name=req.name,email=req.email,password=Hash.bcrypt(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with that id-{id} is not found')
    return user