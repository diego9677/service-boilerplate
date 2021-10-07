from fastapi import Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .auth import Auth
from .db import SessionLocal

security = HTTPBearer()


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def login_required(request: Request, auth: HTTPAuthorizationCredentials = Security(security),
                   session: Session = Depends(get_db)):
    user = Auth.decode_token(auth.credentials, session)
    request.state.user = user
