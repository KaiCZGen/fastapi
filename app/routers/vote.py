from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, database, models, oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_p: schema.Vote, db: Session = Depends(database.get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    post_ext = db.query(models.Post).filter(models.Post.id == vote_p.post_id).first()
    if not post_ext:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with id {vote_p.post_id} does not exists')
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote_p.post_id, models.Votes.user_id == current_user.id)
    vote = vote_query.first()
    
    # like
    if vote_p.post_dir == 1:
        if vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Votes(post_id = vote_p.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "successfully added vote"}
    # dislike
    else:
        if not vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Vote does not exists')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"} 
