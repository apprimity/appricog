import os
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request, Depends, status

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from util.common import fake_users_db, http_basic, HTTPBasicCredentials
from models.user import User, UserCreate

from util.logger import logger


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserCreate(**user_dict)


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token) -> UserCreate:
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(  # token: Annotated[str, Depends(oauth2_scheme)]
    credentials: Annotated[HTTPBasicCredentials, Depends(http_basic)]
):
    user = fake_decode_token(credentials.username)
    if not user:
        # Check if the user is set in the session
        request: Request
        user = request.session["token_response"]["access_token"]
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
