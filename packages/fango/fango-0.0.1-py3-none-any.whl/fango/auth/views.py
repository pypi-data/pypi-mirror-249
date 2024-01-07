from fastapi import Depends, HTTPException, status

from auth.repositories import (
    authenticate_user,
    create_access_token,
    register_user,
    get_request,
)
from fango.routing import public
from auth.schemas import Credentials, Token, User


@public.post("/login/")
async def login(credentials: Credentials, request=Depends(get_request)) -> Token:
    user = await authenticate_user(request, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user)
    return Token(access=access_token)


@public.post("/register/")
async def register(request=Depends(get_request)) -> User:
    payload = await request.json()
    user = await register_user(payload["email"], payload["password"])
    return User.model_validate(user)
