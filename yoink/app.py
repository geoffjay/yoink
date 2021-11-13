import logging
from asyncio import CancelledError
from functools import wraps

import requests
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyppeteer.errors import TimeoutError

from yoink.session import create_session, Session

logger = logging.getLogger("uvicorn.error")


class State(dict):
    name: str = "Yoink!"
    session: Session


app = FastAPI()
state = State()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def session_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not hasattr(state, "session"):
            raise HTTPException(status_code=404, detail="no session is available")
        return await func(*args, **kwargs)

    return wrapper


@app.on_event("shutdown")
async def app_shutdown():
    logger.debug("Executing shutdown callback")
    if hasattr(state, "session"):
        del state.session


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "state": state})


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    try:
        state.session = await create_session()
        await state.session.execute(email, password)
    except TimeoutError as e:
        raise HTTPException(status_code=500, detail=e)
    except CancelledError as e:
        raise HTTPException(status_code=500, detail=e)
    return {"email": email, "success": True}


@app.get("/session/headers")
@session_required
async def session_headers():
    return state.session.headers


@app.get("/session/cookies")
@session_required
async def session_cookies():
    return state.session.cookies


@app.get("/session/requests")
@session_required
async def session_requests():
    response = requests.get(
        f"{state.session.base_url}/api/v4/users/who_am_i",
        # cookies=state.session.cookie_jar,
        headers=state.session.headers,
    )
    return response.json()


@app.get("/session/pyppeteer")
@session_required
async def session_pyppeteer():
    response = await state.session.who_am_i()
    if response is None:
        raise HTTPException(status_code=500, detail="failed to lookup user info")
    content = await response.json()
    return content


@app.post("/session/shutdown")
@session_required
async def session_shutdown():
    del state.session
    return {}
