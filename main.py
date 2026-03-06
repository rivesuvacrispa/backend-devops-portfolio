from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import util
import os

from starlette.responses import HTMLResponse, RedirectResponse

from middlewares import LanguageMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(LanguageMiddleware)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def index(request: Request, lang="ru"):
    return RedirectResponse(request.url_for('about'))



@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, lang="ru"):

    projects, filters = util.load_projects(request.state.lang, ["other-projects", "другие-проекты"])
    profile = util.load_lang_file(request.state.lang, "profile.json")

    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "profile": profile,
            "projects": projects,
        }
    )


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, lang="ru", filter="php"):

    filter = filter.lower()

    projects, filters = util.load_projects(request.state.lang)

    if filter:
        projects = [p for p in projects if p['filter'].lower() == filter]

    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "filters": filters,
            "projects": projects,
            "active_filter": filter
        }
    )


@app.get("/contacts", response_class=HTMLResponse)
async def contacts(request: Request, lang="ru"):


    return templates.TemplateResponse(
        "contacts.html",
        {
            "request": request,
        }
    )