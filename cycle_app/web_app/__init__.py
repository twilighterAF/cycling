import pathlib

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

TEMPLATE_DIR = pathlib.PurePath(__file__).parent.joinpath('templates')
STATIC_DIR = pathlib.PurePath(__file__).parent.joinpath('static')

app = FastAPI()
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
templates = Jinja2Templates(directory=TEMPLATE_DIR)


from cycle_app.web_app.views import *
