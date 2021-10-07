from sqlalchemy import Column, Integer, String, Boolean
from ..db import Model


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String)

    def __repr__(self):
        return f'User(id={self.id} email={self.email})'
