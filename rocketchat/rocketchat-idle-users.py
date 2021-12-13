# -----------------
# Rocketchat Idle Users returns a list of users that have not logged into rocketchat for the past X months
# -----------------

import subprocess
import requests
from rocketchat_API.rocketchat import RocketChat
from pprint import pprint
from datetime import datetime
import dotenv
import os
import json


def get_idle_users():

    # don't forget to check the username and add the password to your environment:
    # export ROCKETCHAT_ADMIN_PASSWORD=XXXXXXXXX

    dotenv.load_dotenv()
    admin_name = 'adminbot'
    admin_pass = os.getenv('ROCKETCHAT_ADMIN_PASSWORD')

    try:
        #rocket = RocketChat(admin_name, admin_pass, server_url='https://chat.developer.gov.bc.ca')

        login_info = {"user": admin_name, "password": admin_pass}
        login_header = {'Content-type': 'application/json'}
        session = requests.Session()
        login_response = session.post("https://chat.developer.gov.bc.ca/api/v1/login",
                                      headers=login_header, data=json.dumps(login_info))
        login_response.raise_for_status()
        auth_header = {"X-Auth-Token": login_response.json()['data']['authToken'],
                       "X-User-Id": login_response.json()['data']['me']['_id']}
        session.headers.update(auth_header)

        current_time = datetime.now()

        active_users = []

        idle_users = {
            '90': {
                'all': [],
                'onetimelogin': []
            },
            '180': {
                'all': [],
                'onetimelogin': []
            },
            '270': {
                'all': [],
                'onetimelogin': []
            },
            '365': {
                'all': [],
                'onetimelogin': []
            },
            'no_username': [],
            'recent_single_login': []
        }

        user_total = 100
        current_user = 0

        while current_user < user_total:

            offset = current_user
            page_params = {"count": 100, "offset": current_user}
            userlist_response = session.get("https://chat.developer.gov.bc.ca/api/v1/users.list", params=page_params)
            userlist_response.raise_for_status()
            user_total = userlist_response.json()['total']
            user_list = userlist_response.json()['users']
            current_user += 100

            for user_id in user_list:
                user_params = {'userId': user_id['_id']}
                user_response = session.get("https://chat.developer.gov.bc.ca/api/v1/users.info",
                                                params=user_params)
                user_response.raise_for_status()
                user = user_response.json()['user']

                # for some reason, not all users have a listed username or lastLogin time, we can skip this
                if 'lastLogin' in user and 'username' in user:

                    last_login = datetime.strptime(user['lastLogin'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    time_since_last_login = current_time - last_login
                    user_created = datetime.strptime(user['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    first_last_login_delta = last_login - user_created

                    if time_since_last_login.days > 365:
                        idle_users['365']['all'].append(user['username'])
                        if first_last_login_delta.days < 2:
                            idle_users['365']['onetimelogin'].append(user['username'])
                    elif time_since_last_login.days > 270:
                        idle_users['270']['all'].append(user['username'])
                        if first_last_login_delta.days < 2:
                            idle_users['270']['onetimelogin'].append(user['username'])
                    elif time_since_last_login.days > 180:
                        idle_users['180']['all'].append(user['username'])
                        if first_last_login_delta.days < 2:
                            idle_users['180']['onetimelogin'].append(user['username'])
                    elif time_since_last_login.days > 90:
                        idle_users['90']['all'].append(user['username'])
                        if first_last_login_delta.days < 2:
                            idle_users['90']['onetimelogin'].append(user['username'])
                    else:
                        active_users.append(user['username'])
                        if first_last_login_delta.days < 2:
                            idle_users['recent_single_login'].append(user['username'])
                else:
                    idle_users['no_username'].append(user['name'])

        print('\n' +
              'Number of users who have not logged into RC in the past 3 months: ' +
              str(len(idle_users['90']['all']) + len(idle_users['180']['all']) + len(idle_users['270']['all']) + len(idle_users['365']['all'])) +
              '\n' +
              ' --> of these, the number who probably only logged in once ever: ' +
              str(len(idle_users['90']['onetimelogin']) + len(idle_users['180']['onetimelogin']) + len(idle_users['270']['onetimelogin']) + len(idle_users['365']['onetimelogin'])) +
              '\n\n' +
              'Number of users who have not logged into RC in the past 6 months: ' +
              str(len(idle_users['180']['all']) + len(idle_users['270']['all']) + len(idle_users['365']['all'])) +
              '\n' +
              ' --> of these, the number who probably only logged in once ever: ' +
              str(len(idle_users['180']['onetimelogin']) + len(idle_users['270']['onetimelogin']) + len(idle_users['365']['onetimelogin'])) +
              '\n\n' +
              'Number of users who have not logged into RC in the past 9 months: ' +
              str(len(idle_users['270']['all']) + len(idle_users['365']['all'])) +
              '\n' +
              ' --> of these, the number who probably only logged in once ever: ' +
              str(len(idle_users['270']['onetimelogin']) + len(idle_users['365']['onetimelogin'])) +
              '\n\n' +
              'Number of users who have not logged into RC in the past year: ' +
              str(len(idle_users['365']['all'])) +
              '\n' +
              ' --> of these, the number who probably only logged in once ever: ' +
              str(len(idle_users['365']['onetimelogin'])) +
              '\n\n' +
              'Number of recent users who have probably only logged in once ever: ' +
              str(len(idle_users['recent_single_login'])) +
              '\n\n' +
              'Number of recently active users: ' +
              str(len(active_users) - len(idle_users['recent_single_login'])) +
              '\n'
              )

    except json.JSONDecodeError as error:
        pprint(error)

    except requests.exceptions.HTTPError as error:
        pprint(error)


get_idle_users()
