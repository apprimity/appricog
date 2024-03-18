from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Request, Depends
from services.inference_services import (
    get_response_and_thought,
    get_response,
    stream_chains,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from util.environment import base_url_prefix, server_host_address, is_prod, app_title
from models.user import User
from util.vector_db_upload import refresh_knowledge_base
from util.logger import logger
from services.login_services import get_current_active_user

# build router
router = APIRouter()
templates = Jinja2Templates(directory="views/templates")


@router.get("/loadData")
async def load_data():
    try:
        return refresh_knowledge_base()
    except Exception as e:
        # Log stack trace
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/chat")
async def chat(
    current_user: Annotated[User, Depends(get_current_active_user)],
    message: str = Query(...),
):
    try:
        return get_response_and_thought(message, current_user)
    except Exception as e:
        # Log stack trace
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/chat-message")
async def chat_message(
    current_user: Annotated[User, Depends(get_current_active_user)],
    message: str = Query(...),
):
    try:
        return get_response(message, current_user)
    except Exception as e:
        # Log stack trace
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/chatbot", response_class=HTMLResponse)
async def chat_bot(
    current_user: Annotated[User, Depends(get_current_active_user)], request: Request
):
    return templates.TemplateResponse(
        # Use "basic_chatbot.html" for another chat UI,
        "chatbot.html",
        {
            "request": request,
            "title": app_title,
            "base_url_prefix": base_url_prefix,
            "assets_url_prefix": (
                (server_host_address + base_url_prefix) if is_prod else ""
            )
            + "/static",
        },
    )


@router.get("/chat-stream")  # TODO: Need to fix this
async def chat_streaming_output(
    current_user: Annotated[User, Depends(get_current_active_user)],
    message: str = Query(...),
):
    # Set the response headers for streaming
    headers = {
        "Content-Type": "text/plain",
        "Transfer-Encoding": "chunked",
    }
    return StreamingResponse(stream_chains(message, current_user), headers=headers)
