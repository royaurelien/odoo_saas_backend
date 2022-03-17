# -*- coding: utf-8 -*-
# Part of SaaS Backend. See LICENSE file for full copyright and licensing details.


from celery import chain, group
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
import os
from typing import Optional

from worker import main as wk
from . import utils

DEFAULT_DUMP_FS = os.environ.get("DUMP_FILESTORE", False)
DEFAULT_DUMP_FORMAT = os.environ.get("DUMP_FORMAT", "sql")


router = APIRouter()


@router.post("/dump", status_code=201)
def run_task_dump(payload = Body(...)):
    data = {'db_name': payload["name"]}

    filestore = payload.get('filestore', DEFAULT_DUMP_FS)
    dump = payload.get('dump', DEFAULT_DUMP_FORMAT)

    tasks = chain(
        wk.create_env.s(data),
        wk.create_odoo_manifest.s(),
        wk.dump_db.s(),
        wk.add_to_zip.s(),
        # wk.add_filestore.s(data).set(link_error=wk.error_handler.s()),
        wk.add_filestore.s(),
        wk.clean_workdir.s(),
    ).on_error(wk.error_handler.s()).apply_async()

    result = {
        "task_id": tasks.id,
        "parent_id": [t.id for t in list(utils.unpack_parents(tasks))][-1],
        # "all": store(tasks)
    }
    return JSONResponse(result)



@router.get("/download/{task_id}")
async def fast_download(task_id: str, method: Optional[str] = None):

    try:
        filepath = utils._get_file_from_task(task_id)
    except ValueError as error:
        return JSONResponse({'status': error})

    if method == "stream":
        return StreamingResponse(utils.iterfile(filepath), media_type="application/octet-stream")

    return FileResponse(filepath)


@router.post("/restore", status_code=201)
def restore_backup(payload = Body(...)):
    data = {
        'db_name': payload["name"],
        'filename': payload["filename"]
    }

    tasks = chain(
        wk.init_restore.s(data),
        wk.unzip_dump.s(),
        wk.create_database.s(),
        wk.restore_dump.s(),
        wk.unzip_filestore.s()
    ).apply_async()

    result = {
        "task_id": tasks.id,
        "parent_id": [t.id for t in list(utils.unpack_parents(tasks))][-1],
        # "names": [item.name for item in list(map(lambda x: x.name, tasks))],
        "names": [t.name for t in list(utils.unpack_parents(tasks))],
        # "all": store(tasks)
    }
    # print([item.name for item in list(map(lambda x: x.name, tasks))])
    return JSONResponse(result)