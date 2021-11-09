from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from yoink.session import create_session

app = FastAPI()
session = create_session()

state = {
    "name": "Yoink",
}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "state": state})


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    return {"email": email, "password": password}
