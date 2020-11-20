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

        user_types = {
            'gov_email': [],
            'other_email': [],
            'no_email': [],
            'no_username': []
        }

        for user in rocket.users_list(count=0).json()['users']:

            # for some reason, not all users have a listed username or createdAt time, we can skip these.
            if 'username' in user and 'emails' in user:
                for email in user['emails']:
                    # add to the gov email list if the email has the right ending and the username isn't already there.
                    if '@gov.bc.ca' in email['address'] and user['username'] not in user_types['gov_email']:
                        user_types['gov_email'].append(user['username'])
                    # otherwise just add the user to the other emails list.
                    elif user['username'] not in user_types['other_email']:
                        user_types['other_email'].append(user['username'])
            elif 'username' in user:
                user_types['no_email'].append(user['username'])
            else:
                user_types['no_username'].append(user['name'])


        print('\n' +
              'Number of users with gov email addresses: ' +
              str(len(user_types['gov_email'])) +
              '\n' +
              'Number of users with other email addresses: ' +
              str(len(user_types['other_email'])) +
              '\n' +
              'Number of users with no listed email address: ' +
              str(len(user_types['no_email'])) +
              '\n')

    except json.JSONDecodeError:
        pprint(json.JSONDecodeError)


get_new_users()
