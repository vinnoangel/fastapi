from fastapi import FastAPI, status, HTTPException
from typing import Optional
from random import randrange
from fastapi.params import Body
from pydantic import BaseModel
from starlette.responses import Response


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "This is the first title", "content": "This is the first content", "id": 1, "published": True, "rating": 3},
    {"title": "This is the second title", "content": "This is the second content", "id": 2, "published": False, "rating": 5}
]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i


@app.get("/")
def root():
    return {"data": "Hi, welcome to FASTAPI!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts, "message": "successful"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    return {"data": post, "message": "successful"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    formatted_post = post.dict()
    formatted_post['id'] = randrange(0, 1000000)
    my_posts.append(formatted_post)
    return {"data": formatted_post, "message": "Post created successfully"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    formatted_post = post.dict()
    formatted_post['id'] = id
    my_posts[index] = formatted_post
    return {"data": formatted_post, "message": "Post updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)