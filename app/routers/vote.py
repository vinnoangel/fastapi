from typing import List, Optional
from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)   
    new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
    is_vote = vote_query.first()
  
    if is_vote:
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
    else:
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}