from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/user',
                   tags=['users'],
                   responses={404: {'message': 'Not found'}})


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {'message': 'User not found'}


# User entity
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name='Johan', surname='Guerra', url='https://github.com/popetasmixs', age=18),
              User(id=2, name='Pepe', surname='Perez',
                   url='https://github.com/pepe', age=20),
              User(id=3, name='Juan', surname='Gomez', url='https://github.com/juan', age=25)]


@router.get('/usersjson')
async def usersjson():
    return [{'name': 'Johan', 'surname': 'Guerra', 'url': 'https://github.com/popetasmixs', 'age': 18},
            {'name': 'Pepe', 'surname': 'Perez',
                'url': 'https://github.com/pepe', 'age': 20},
            {'name': 'Juan', 'surname': 'Gomez', 'url': 'https://github.com/juan', 'age': 25}]


@router.get('/users')
async def usersclass():
    return users_list


# Path
@router.get('/{id}')
async def user(id: int):
    return search_user(id)


# Query
@router.get('/userquery')
async def user(id: int):
    return search_user(id)


@router.post('/', status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail='The user already exists')
    else:
        users_list.append(user)
        return user


@router.put('/', status_code=201)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        raise HTTPException(status_code=404, detail='The user was not updated')
    else:
        return user


@router.delete('/{id}', status_code=200)
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail='The user was not deleted')
    else:
        return {'message': 'User deleted'}
