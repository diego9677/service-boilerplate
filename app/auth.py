import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
# models and db
from .models import User
from settings import settings


class Auth:
    hasher = CryptContext(schemes=['bcrypt'])
    secret = settings.SECRET_KEY

    @classmethod
    def verify_password(cls, password: str, encoded_password: str):
        return cls.hasher.verify(password, encoded_password)

    @classmethod
    def encode_password(cls, password: str):
        return cls.hasher.hash(password)

    @classmethod
    def encode_token(cls, sub):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': sub
        }
        return jwt.encode(payload, cls.secret, algorithm='HS256')

    @classmethod
    def decode_token(cls, token: str, db: Session):
        try:
            payload = jwt.decode(token, cls.secret, algorithms=['HS256'])
            if payload['scope'] == 'access_token':
                stmt = select(User).filter_by(email=payload['sub'], is_active=True)
                user_db = db.execute(stmt).scalars().first()
                if not user_db:
                    detail = {'code': 'not_found', 'msg': 'User not found or not active'}
                    raise HTTPException(status_code=404, detail=detail)
                return user_db
            detail = {'code': 'invalid_scope', 'msg': 'Scope for the token is invalid'}
            raise HTTPException(status_code=401, detail=detail)
        except jwt.ExpiredSignatureError:
            detail = {'code': 'expired_token', 'msg': 'Token expired'}
            raise HTTPException(status_code=401, detail=detail)
        except jwt.InvalidTokenError:
            detail = {'code': 'invalid_token', 'msg': 'Invalid token'}
            raise HTTPException(status_code=401, detail=detail)

    @classmethod
    def encode_refresh_token(cls, sub):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=10),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': sub
        }
        return jwt.encode(payload, cls.secret, algorithm='HS256')

    @classmethod
    def decode_refresh_token(cls, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, cls.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                sub = payload['sub']
                new_token = cls.encode_token(sub)
                return new_token
            raise HTTPException(status_code=401, detail={'code': 'invalid_scope', 'msg': 'Invalid scope for token'})

        except jwt.ExpiredSignatureError:
            detail = {'code': 'expired_refresh_token', 'msg': 'Refresh token expired'}
            raise HTTPException(status_code=401, detail=detail)
        except jwt.InvalidTokenError:
            detail = {'code': 'invalid_refresh_token', 'msg': 'Invalid refresh token'}
            raise HTTPException(status_code=401, detail=detail)
