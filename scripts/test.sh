#!/bin/sh
# Part of Odoo SaaS Backend. See LICENSE file for full copyright and licensing details.


# curl http://localhost:8004/api/v1/odoo/restore -H "Content-Type: application/json" --data '{"name": "toiles-chics", "filename": "TOILESCHICS-PROD_20220124_0929.zip"}'
# curl http://localhost:8004/api/v1/odoo/dump -H "Content-Type: application/json" --data '{"name": "toiles"}'
curl http://localhost:8004/api/v1/odoo/duplicate -H "Content-Type: application/json" --data '{"name": "toiles-chics", "new":"test-toiles-chics"}'