from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..serializers import TokenOut, RefreshToken, Login, RefreshTokenOut
from ..dependencies import get_db
from ..models import User
from ..auth import Auth

router = APIRouter(prefix='/api/token', tags=['token'])


# auth endpoints
@router.post('', response_model=TokenOut)
def generate_access_token(body: Login, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == body.email)
    user_db = db.execute(stmt).scalars().first()
    if not user_db:
        raise HTTPException(status_code=400, detail={'code': 'invalid_email', 'msg': 'Invalid email'})

    if not Auth.verify_password(password=body.password, encoded_password=user_db.password):
        raise HTTPException(status_code=400, detail={'code': 'invalid_password', 'msg': 'Invalid password'})

    if not user_db.is_active:
        raise HTTPException(status_code=400, detail={'code': 'invalid_user', 'msg': 'Invalid user'})

    token = Auth.encode_token(user_db.email)
    refresh = Auth.encode_refresh_token(user_db.email)
    return TokenOut(access=token, refresh=refresh)


@router.post('/refresh', response_model=RefreshTokenOut)
def generate_refresh_token(body: RefreshToken):
    new_access_token = Auth.decode_refresh_token(body.refresh)
    return RefreshTokenOut(access=new_access_token)
