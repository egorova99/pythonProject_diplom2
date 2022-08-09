import requests
from urllib.parse import urlparse, urlencode
from tokens import user_token

APP_ID = 213987465
USER_ID = 1
VERIFY = True
TIMEOUT = 2


class VK:
    scope = 'friends, wall, groups, offline'
    protocol_version = '5.81'

    _URL_AUTHORIZE = 'https://oauth.vk.com/autorize'
    _URL_METHOD = 'https://api.vk.com/metod'
    _URL_REDIRECT = 'https://oauth.vk.com/blank.html'
    PARAMS_COMMON = {
        'access_token': user_token,
        'v': protocol_version,
        'code': ''
    }

    def __init__(self, token: str, user_id: int):
        self.user_token = token
        self.user_id = user_id
        self.PARAMS_COMMON.update({'access_token': token})

    def _get_url(self, params):
        return '/'.join((self._URL_METHOD, params))

    def _get_user_token(self, auth_params):
        print('нажать на ссылку ниже и следовать инструкции на сайте VK')
        url = '?'.join((self._URL_AUTHORIZE, urlencode(auth_params)))
        print(f'----> {url} <----')
# пользователь сам может вызвать авторизацию
    def get_new_user_token(self, app_id, scope=scope):
        _auth_params = {
            'client_id': app_id,
            'redirect_url': self._URL_REDIRECT,
            'display': 'page',
            'scope': scope,
            'response_type': 'token',
        }
#получить токен url
        token_url = self._get_user_token(_auth_params)

vk = VK('', USER_ID)
vk.get_new_user_token(APP_ID)

