from fastapi import FastAPI, status, HTTPException
from typing import Optional
from random import randrange
from fastapi.params import Body
from pydantic import BaseModel
from starlette.responses import Response
import mysql.connector
from mysql.connector import Error
import time
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='fastapi',
            username='root',
            password=''
        )

        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Error as error:
        print("Error connecting to databse", error)
        print("Reconnecting...")
        time.sleep(2)


@app.get("/")
def root():
    return {"data": "Hi, welcome to FASTAPI!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts, "message": "successful"}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    return {"data": post, "message": "successfully"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (post.title, post.content, post.published))
    conn.commit()
    
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(cursor.lastrowid),))
    post = cursor.fetchone()

    return {"data": post, "message": "Post created successfully"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post_exist = cursor.fetchone()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    return {"data": post_exist, "message": "Post updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)