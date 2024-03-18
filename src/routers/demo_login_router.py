import os
import logging, requests
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from util.environment import base_url_prefix, server_host_address, is_prod
from util.common import __version__, fake_users_db, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm, HTTPBasicCredentials
from models.user import User, UserCreate
from services.login_services import fake_hash_password, get_current_active_user
from util.logger import logger

# build router
router = APIRouter()
templates = Jinja2Templates(directory="views/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("demo_login.html", {"request": request})


@router.post("/token")
async def login(
    form_data: Annotated[HTTPBasicCredentials, Depends()], request: Request
):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserCreate(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token_response = {"access_token": user.username, "token_type": "bearer"}

    return RedirectResponse(request.url_for("chatbot"))


@router.get("/users/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
