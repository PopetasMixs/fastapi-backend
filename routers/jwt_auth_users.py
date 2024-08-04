from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = "b66720de3cd3b8521c6190d26479fb7defc6eac9744d1e8541f0ab5d32ef0f6e"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=['bcrypt'])


# User entity
class UserDTO(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDAO(UserDTO):
    password: str


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@gmail.com",
        "disabled": False,
        "password": "$2a$12$fZX7zk7Ag5dqQ1MP4ZOyvujLra8ktql0AeQ04MzXYvH6h9BEIui8W"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alicewonder@gmail.com",
        "disabled": True,
        "password": "$2a$12$rZE9I8Q4FX.sbueNB9F1KuKOgDbnO0ZJalsgqw6WwqY8KTS6RjJxO"
    }
}


def search_user_dao(username: str):
    if username in users_db:
        return UserDAO(**users_db[username])


@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    user = search_user_dao(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    acces_token = {'sub': user.username,
                   'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {'access_token': jwt.encode(acces_token, SECRET_KEY, algorithm=ALGORITHM), 'token_type': 'bearer'}
