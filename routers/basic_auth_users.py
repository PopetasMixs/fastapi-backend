from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl='login')


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
        "password": "secret123"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alicewonder@gmail.com",
        "disabled": True,
        "password": "secret456"
    }
}


def search_user_dao(username: str):
    if username in users_db:
        return UserDAO(**users_db[username])


def search_user_dto(username: str):
    if username in users_db:
        return UserDTO(**users_db[username])


def current_user(token: str = Depends(oauth2)):
    user = search_user_dto(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Auth credentials invalid',
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user')
    return user


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail='Incorrect username')

    user = search_user_dao(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail='Incorrect password')

    return {'access_token': user.username, 'token_type': 'bearer'}


@router.get('/users/me')
async def me(user: UserDAO = Depends(current_user)):
    return user
