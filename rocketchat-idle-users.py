# -----------------
# Rocketchat Idle Users returns a list of users that have not logged into rocketchat for the past X months
# -----------------

import subprocess
from rocketchat_API.rocketchat import RocketChat
from pprint import pprint
from datetime import datetime
import dotenv
import os
import json


def get_idle_users():

    dotenv.load_dotenv()
    admin_pass = os.getenv('ROCKETCHAT_ADMIN_PASSWORD')

    try:
        rocket = RocketChat('admin', admin_pass, server_url='https://chat.pathfinder.gov.bc.ca')

        current_time = datetime.now()

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
            'no_username': []
        }

        for user in rocket.users_list(count=0).json()['users']:
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
              '\n'
              )



    except json.JSONDecodeError:
        pprint(json.JSONDecodeError)



get_idle_users()
