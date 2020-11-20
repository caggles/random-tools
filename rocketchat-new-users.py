# -----------------
# Rocketchat New Users returns information about users that have recently joined RC
# -----------------

import subprocess
from rocketchat_API.rocketchat import RocketChat
from pprint import pprint
from datetime import datetime
import dotenv
import os
import json


def get_new_users():

    dotenv.load_dotenv()
    admin_pass = os.getenv('ROCKETCHAT_ADMIN_PASSWORD')

    try:
        rocket = RocketChat('admin', admin_pass, server_url='https://chat.pathfinder.gov.bc.ca')

        current_time = datetime.now()

        new_users = {
            '30': [],
            '60': [],
            '90': [],
            '120': [],
            '150': [],
            '180': [],
            'older': [],
            'no_username': []
        }

        for user in rocket.users_list(count=0).json()['users']:

            # for some reason, not all users have a listed username or createdAt time, we can skip these.
            if 'createdAt' in user and 'username' in user:

                user_created = datetime.strptime(user['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                time_since_created = current_time - user_created

                if time_since_created.days > 180:
                    new_users['older'].append(user['username'])
                elif time_since_created.days > 150:
                    new_users['180'].append(user['username'])
                elif time_since_created.days > 120:
                    new_users['150'].append(user['username'])
                elif time_since_created.days > 90:
                    new_users['120'].append(user['username'])
                elif time_since_created.days > 60:
                    new_users['90'].append(user['username'])
                elif time_since_created.days > 30:
                    new_users['60'].append(user['username'])
                elif time_since_created.days > 0:
                    new_users['30'].append(user['username'])
            else:
                new_users['no_username'].append(user['name'])

        average = round((len(new_users['30']) +
                   len(new_users['60']) +
                   len(new_users['90']) +
                   len(new_users['120']) +
                   len(new_users['150']) +
                   len(new_users['180']))/6)

        print('\n' +
              'Number of users created past month: ' +
              str(len(new_users['30'])) +
              '\n' +
              'Number of users created 1-2 months ago: ' +
              str(len(new_users['60'])) +
              '\n' +
              'Number of users created 2-3 months ago: ' +
              str(len(new_users['90'])) +
              '\n' +
              'Number of users created 3-4 months ago: ' +
              str(len(new_users['120'])) +
              '\n' +
              'Number of users created 4-5 months ago: ' +
              str(len(new_users['150'])) +
              '\n' +
              'Number of users created 5-6 months ago: ' +
              str(len(new_users['180'])) +
              '\n' +
              'Average number of users created per month in the past 6 months: ' +
              str(average) +
              '\n'
              )

    except json.JSONDecodeError:
        pprint(json.JSONDecodeError)


get_new_users()
