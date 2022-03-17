# -*- coding: utf-8 -*-
# Part of SaaS Backend. See LICENSE file for full copyright and licensing details.

from celery.result import AsyncResult
from celery import chain, group
from fastapi import Body, FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import os

from api.v1.api import api_router
from core.config import settings
from api.v1.endpoints import utils

DEFAULT_DUMP_FS = os.environ.get("DUMP_FILESTORE", False)
DEFAULT_DUMP_FORMAT = os.environ.get("DUMP_FORMAT", "sql")


root_router = APIRouter()
app = FastAPI(title="SaaS Backend")

@root_router.get("/", status_code=200)
def root(request: Request):
    vals = {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
    }
    return JSONResponse(vals)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)