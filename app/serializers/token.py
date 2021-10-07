from pydantic import BaseModel


# inputs
class Login(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'admin@admin.com',
                'password': 'admin12345'
            }
        }


class RefreshToken(BaseModel):
    refresh: str

    class Config:
        schema_extra = {
            'example': {
                'refresh': 'refresh-token-generated'
            }
        }


# outputs
class TokenOut(BaseModel):
    access: str
    refresh: str

    class Config:
        schema_extra = {
            'example': {
                'access': 'access-token-generated',
                'refresh': 'refresh-token-generated'
            }
        }


class RefreshTokenOut(BaseModel):
    access: str

    class Config:
        schema_extra = {
            'example': {
                'access': 'access-token-generated'
            }
        }
