# -----------------
# Rocketchat Integrations returns information about a particular RC integration
# -----------------

import subprocess
import requests
from pprint import pprint
import dotenv
import os
import json


def get_new_users():

    dotenv.load_dotenv()
    admin_pass = os.getenv('ROCKETCHAT_ADMIN_PASSWORD')

    try:

        login_response = requests.post(
            "https://chat.pathfinder.gov.bc.ca/api/v1/login",
            data={'user': 'admin',
                  'password': admin_pass})

        token = login_response.json()['data']['authToken']
        uid = login_response.json()['data']['userId']

        print(token)
        print(uid)

        integ_list = requests.get(
            "https://chat.pathfinder.gov.bc.ca/api/v1/integrations.list",
            headers={'X-Auth-Token': token,
                     'X-User-Id': uid,
                     'Content-type': 'application/json'},
            params={'count': 0})

        print(' ')

        for integration in integ_list.json()['integrations']:
            if integration['_createdBy']['username'] == 'cailey.jones':
                print(integration['name'] + ' (' + integration['type'] + '):' +
                      '\n     --> channel: ' + ','.join(integration['channel']) +
                      '\n     --> ID: ' + integration['_id'] +
                      '\n     --> token: ' + integration['token'] +
                      '\n')



    except json.JSONDecodeError:
        pprint(json.JSONDecodeError)


get_new_users()
