from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)


@app.get('/')
async def root():
    return 'Hello FastAPI!'


@app.get('/url')
async def url():
    return {'url': 'https://github.com/popetasmixs'}
