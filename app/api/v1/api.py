# -*- coding: utf-8 -*-
# Part of SaaS Backend. See LICENSE file for full copyright and licensing details.

from fastapi import APIRouter

from .endpoints import odoo, tasks


api_router = APIRouter()
api_router.include_router(odoo.router, prefix="/odoo", tags=["odoo"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])