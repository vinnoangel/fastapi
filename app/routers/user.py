from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/users', 
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user, "message": "User created successfully"}


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"data": users, "message": "successful"}


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user ID {id} not found")

    return {"data": user, "message": "successful"}