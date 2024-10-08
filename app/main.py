from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
        {
            "title": "title post 1",
            "content": "post content",
            "id": 1
        },

        {
            "title": "Tetris",
            "content": "4 line combo",
            "id": 2
        },
    ]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.get('/posts/{id}')
async def get_specific_post(id: int, response : Response):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} was not found"
            )
    
    return {"post_details": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} did not exist")
            
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} did not exist")
            
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
