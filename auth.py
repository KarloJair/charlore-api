from datetime import timedelta, datetime, UTC
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['argon2'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    create_user_request: CreateUserRequest,
    db: db_dependency
):
    
    create_user_model = User(
        username=create_user_request.username,
        password=bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
    ):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="No se ha podido verificar el usuario")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type':'bearer'}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return None
    if not bcrypt_context.verify(password, user.password):
        return None
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    
    payload = {
        "sub": username,
        "id": user_id,
        "exp": datetime.now(UTC) + expires_delta
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get('sub')
        user_id: int | None = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se ha podido verificar el usuario")
        return {
            'username':username, 
            'id':user_id
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se ha podido verificar el usuario"
        )