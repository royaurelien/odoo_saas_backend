#!/usr/bin/python3

import requests
import time
import sys

base_url = 'http://localhost:8004/api/v1/{}'


def post_api(action, data):
    r = requests.post(base_url.format(action), json=data)
    response = r.json()

    return response

def get_api(action):
    r = requests.get(base_url.format(action))
    response = r.json()

    return response

def run_restore(db_name, filename):
    payload = {
        'name': db_name,
        "filename": filename,
    }

    response = post_api('odoo/restore', payload)

    task_id = response.get('task_id')
    parent_id = response.get('parent_id')

    if not all([task_id, parent_id]):
        print(response)
        sys.exit(1)

    print("Restore '{}' with {}".format(db_name, filename))
    print(response)

    while True:
        resp = get_api('tasks/{}'.format(parent_id))
        if resp:
            print(resp)
        time.sleep(2)


if __name__ == '__main__':
    run_restore("toiles2", "TOILESCHICS-PROD_20220124_0929.zip")