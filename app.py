# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    app.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: msabwat <msabwat@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/03/29 11:36:55 by msabwat           #+#    #+#              #
#    Updated: 2018/04/26 17:04:39 by msabwat          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import requests
import re
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
fb_access_token="" ##Value to complete by creating a developper account on facebook or implementing OAUTH?

@app.route('/')

def hello():
    return 'User Status challenge'

def get_byid(response, host, uid):
    r = requests.get("https://graph.facebook.com/v2.12/" + uid + "?fields=link,name&access_token=" + fb_access_token)
    if r.status_code == 200:
        data = r.json()
        response['account_handle'] = data['name']
        response['account_url'] = data['link']
        response['status'] = "up"
    elif r.status_code == 190:
        response['status'] = "Invalid token" #implement a refresh ?
    else:
        response['account_handle'] = 'Not Found'
        response['account_url'] = 'Not Found'
        response['status'] = "down"
    return response

def get_byhandle(response, host, uid):
    r = requests.get("https://facebook.com/" + uid)
    data = str(r)
    r = re.search('fb:\/\/profile\/(.+?)', data)
    if 'profile' in str(r):
        response['account_id'] = str(r)
        response['account_url'] = "https://facebook.com/"+ uid
        response['status'] = "up"
    else:
        r = re.search('\/help\/\?ref\=404', data)
        if  '404' in str(r):
            response['account_id'] = 'Not found'
            response['account_url'] = 'Not found'
            response['status'] = "down"
        else:
            response['status'] = "Unknown error"
    return response

def get_byurl(response, host, uid):
    response['account_id'] = ''
    response['account_handle'] = ''
    response['status'] = ''
    return response

def handle_request(host, uid, uid_type):
    response = {}
    response['hostingparty'] = host
    if 'id' in uid_type:
        response['account_id'] = uid
        response = get_byid(response, host, uid)
    elif 'handle' in uid_type:
        response['account_handle'] = uid
        response = get_byhandle(response, host, uid)
    elif 'url' in uid_type:
        response['account_url'] = uid
        response = get_byurl(response, host, uid)
    return response

def handle_input(host, user_id):
    if 'id=' in user_id:
        user_id = user_id.split('=', 1)
        uid = user_id[1]
        id_type = user_id[0]
    elif 'handle=' in user_id:
        user_id = user_id.split('=', 1)
        uid = user_id[1]
        id_type = user_id[0]
    elif 'url=' in user_id:
        user_id = user_id.split('=', 1)
        uid = user_id[1]
        id_type = user_id[0]
    else:
        return 'Error, invalid request'
    return handle_request(host, uid, id_type)


class UserStatus(Resource):
    def get(self, host, user_id):
        return handle_input(host, user_id)


api.add_resource(UserStatus, '/user_status/<host>/<user_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
