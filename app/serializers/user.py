from typing import Optional
from pydantic import BaseModel, root_validator


class UserIn(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'spongebob@mail.com',
                'first_name': 'Spongebob',
                'last_name': 'Squarepants',
                'password': 'your-password'
            }
        }


class UserUpdateIn(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'email': 'spongebob@mail.com',
                'first_name': 'Spongebob',
                'last_name': 'Squarepants',
                'is_active': True
            }
        }


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    events: Optional[int]

    @root_validator
    def get_events(cls, values):
        values['events'] = sum([1, 2, 3])
        return values

    class Config:
        orm_mode = True

        schema_extra = {
            'example': {
                'id': 1,
                'email': 'spongebob@mail.com',
                'first_name': 'Spongebob',
                'last_name': 'Squarepants',
                'is_active': True
            }
        }


class Message(BaseModel):
    msg: str

    class Config:
        schema_extra = {
            'example': {
                'msg': 'Message of confirmation'
            }
        }
