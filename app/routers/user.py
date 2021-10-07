from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from ..dependencies import get_db, login_required
from ..serializers import UserIn, UserUpdateIn, UserOut, Message
from ..models import User
from ..auth import Auth

router = APIRouter(prefix='/api/users', tags=['users'], dependencies=[Depends(login_required)])


@router.get('', response_model=List[UserOut])
def read_users(request: Request, db: Session = Depends(get_db)):
    print(request.state.user)
    stmt = select(User).order_by(User.id.asc())
    return db.execute(stmt).scalars().all()


@router.post('', response_model=UserOut)
def create_user(request: Request, body: UserIn, db: Session = Depends(get_db)):
    print(request.state.user)
    body.password = Auth.encode_password(body.password)
    user_db = User(**body.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@router.get('/whoiam', response_model=UserOut)
def whoiam(request: Request):
    return request.state.user


@router.get('/{id_user}', response_model=UserOut)
def get_user(id_user: int, request: Request, db: Session = Depends(get_db)):
    print(request.state.user)
    stmt = select(User).where(User.id == id_user)
    user_db = db.execute(stmt).scalars().first()
    if not user_db:
        raise HTTPException(status_code=404, detail={'msg': f'User {id_user} not found.'})
    return user_db


@router.put('/{id_user}', response_model=UserOut, description="optional password")
def update_user(id_user: int, request: Request, body: UserUpdateIn, db: Session = Depends(get_db)):
    print(request.state.user)
    if body.password:
        body.password = Auth.encode_password(body.password)
    stmt = select(User).where(User.id == id_user)
    user_db = db.execute(stmt).scalars().first()
    if not user_db:
        raise HTTPException(status_code=404, detail={'msg': f'User {id_user} not found.'})

    result = db.execute(update(User).where(User.id == id_user).values(**body.dict(exclude_unset=True)))
    db.commit()
    db.refresh(user_db)
    if result.rowcount == 1:
        return user_db
    raise HTTPException(status_code=500)


@router.delete('/{id_user}', response_model=Message)
def delete_user(id_user: int, request: Request, db: Session = Depends(get_db)):
    print(request.state.user)
    user_db: User = db.query(User).filter_by(id=id_user).first()

    if not user_db:
        raise HTTPException(status_code=404, detail={'msg': f'User {id_user} not found.'})
    result = db.execute(delete(User).where(User.id == id_user))
    db.commit()
    if result.rowcount == 1:
        return Message(msg=f'User {id_user} deleted successfully.')
    raise HTTPException(status_code=500)
