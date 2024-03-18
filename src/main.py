import uvicorn
from routers.inference_router import router as inference_router
from routers.demo_login_router import router as demo_login_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from util.environment import base_url_prefix, app_title
from starlette.middleware.sessions import SessionMiddleware


def create_app():
    """Create the FastAPI app and include the router."""
    app = FastAPI(title=app_title, root_path=base_url_prefix)
    app.mount("/static", StaticFiles(directory="views/static"), name="static")

    origins = [
        "*",
    ]

    # CORS middleware to allow CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Session middleware to auto login with the help of a cookie
    app.add_middleware(
        SessionMiddleware,
        secret_key="$3cret_K3y",
        session_cookie="3cret_c00k13",
        # session_ttl=3600,  # Session TTL in seconds (e.g., 1 hour)
    )

    app.include_router(inference_router)
    app.include_router(demo_login_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7889, reload=True)
