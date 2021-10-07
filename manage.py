import typer
from sqlalchemy.orm import Session
from getpass import getpass
from app.auth import Auth
from app.db import SessionLocal
from app.models import User

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f'Hello {name}')


@app.command()
def createsuperuser():
    typer.echo('Create super user')
    email = typer.prompt('Email')
    first_name = typer.prompt('First Name')
    last_name = typer.prompt('Last Name')
    password = getpass('Password: ')
    db: Session = SessionLocal()
    try:
        user_db = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Auth.encode_password(password),
            is_admin=True)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        typer.echo(f'User {user_db.id} created successfully')
    finally:
        db.close()


if __name__ == '__main__':
    app()
