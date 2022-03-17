# -*- coding: utf-8 -*-
# Part of SaaS Backend. See LICENSE file for full copyright and licensing details.

from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    app_name: str = "SaaS Backend API"
    admin_email: str = "roy.aurelien@gmail.com"


settings = Settings()