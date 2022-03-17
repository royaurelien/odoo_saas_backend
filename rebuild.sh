#!/bin/sh
# Part of Odoo SaaS Backend. See LICENSE file for full copyright and licensing details.

docker-compose down
docker-compose up -d --build


# -e CELERY_BROKER_URL='redis://redis:6379/0' -e CELERY_RESULT_BACKEND='redis://redis:6379/0' -e POSTGRES_PASSWORD='odoo' -e POSTGRES_USER='odoo' -e POSTGRES_HOST='db' -e POSTGRES_HOST='5432'