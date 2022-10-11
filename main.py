from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/blogs')
def index(limit,published: bool=True,sort: Optional[str]=None):
    if published:
        return {"data": f'{limit} Published blog form the db'}
    else:
        return {"data": f'{limit} Unpublished blog form the db'}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data': {'1','2'}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog/')
def create_blog(req: Blog):
    return f'Blog is created with Title as {req.title}'

