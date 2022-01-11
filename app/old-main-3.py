import psycopg2
from fastapi import FastAPI, status, Response, HTTPException, Depends
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='pass1234',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Error connecting to databse", error)
        print("Reconnecting...")
        time.sleep(2)


@app.get("/")
def root():
    return {"data": "Hi, welcome to FASTAPI!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts, "message": "successful"}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    return {"data": post, "message": "successfully"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # conn.commit()
    # post = cursor.fetchone()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post, "message": "Post created successfully"}


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first(), "message": "Post updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user, "message": "User created successfully"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"data": users, "message": "successful"}


@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user ID {id} not found")

    return {"data": user, "message": "successful"}


# def create_user(db: Session, user: schemas.AccountsCreate):
#     db_user = models.AccountsInfo(user_name=user.user_name, password=user.password, email=user.email,created_on=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),allow=True)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
