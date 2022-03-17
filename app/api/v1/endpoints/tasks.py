# -*- coding: utf-8 -*-
# Part of SaaS Backend. See LICENSE file for full copyright and licensing details.


from celery.result import AsyncResult
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from typing import Optional

from worker import main as wk
from . import utils

router = APIRouter()


@router.get("/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)

    result = {
        "id": task_id,
        "result": str(task_result.result) if bool(task_result.traceback) else task_result.result,
        "traceback": str(task_result.traceback) if task_result.traceback else "",
        "status": task_result.status,
        "tasks": [(t.name, t.state) for t in utils.iter_children(task_result)],
    }
    # task_result.forget()
    return JSONResponse(result)