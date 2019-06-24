import requests

def start_Url_code():

        payload = {'client_id': '7021952',
                   'display': 'page',
                   'redirect_uri': 'http://127.0.0.1:8000/vkontakte',
                   'client_secret': 'stIHRvDcAxhPTA4WO43g',
                   'scope': 'notify',
                   'response_type': 'code',
                   'v': '5.95'
                   }

        r = requests.get('http://oauth.vk.com/authorize', params=payload)
        return (r)

def start_Url_access_token(code):

    payload = {'client_id': '7021952',
               'client_secret': 'stIHRvDcAxhPTA4WO43g',
               'redirect_uri': 'http://127.0.0.1:8000/vkontakte',
               'code': str(code)
               }

    r = requests.get('https://oauth.vk.com/access_token', params=payload)
    return (r)

def start_request_API(token, user_id):

    payload = {'user_ids': str(user_id),
               'fields': 'bdate',
               'access_token': str(token),
               'v': '5.95'
               }

    r = requests.get('https://api.vk.com/method/users.get', params=payload)
    return (r)

