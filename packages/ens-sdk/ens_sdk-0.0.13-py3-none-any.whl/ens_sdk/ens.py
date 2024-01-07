import base64
import json
from datetime import timedelta, datetime

import requests
import sentry_sdk

from .utils.cache import Cache
from decouple import config
from .utils.timezone import make_aware


class ENS:

    def __init__(self):
        self._CLIENT_ID = config('ENCIPHER_CLIENT_ID')
        self._CLIENT_SECRET = config('ENCIPHER_CLIENT_SECRET')
        self._ENS_SERVER = config('ENCIPHER_ENS_SERVER')
        self._ENS_PORT = config('ENCIPHER_ENS_PORT')
        self._API_VERSION = config('ENCIPHER_API_VERSION')
        self._cache = Cache()

    @staticmethod
    def _expires_in(expires_in: bytes, last_updated_at: bytes):
        # @todo replace django's make_aware() with python builtins
        time_elapsed = datetime.now() - make_aware(datetime.fromtimestamp(int(float(last_updated_at))))
        left_time = timedelta(seconds=int(expires_in)) - time_elapsed
        return left_time

    def _is_token_expired(self):
        _d = self._cache.retrieve(self._ENS_SERVER)
        _cache_data = json.loads(_d) if _d else {}
        expires_in = _cache_data.get('expires_in', None)
        last_updated_at = _cache_data.get('last_updated_at', None)
        return self._expires_in(expires_in, last_updated_at) < timedelta(seconds=0) if last_updated_at and expires_in else True

    def token_expire_handler(self):
        is_expired = self._is_token_expired()
        if is_expired: self._get_auth_token()
        return is_expired

    def _get_auth_token(self):
        credentials = "{0}:{1}".format(self._CLIENT_ID, self._CLIENT_SECRET)
        authorization = base64.b64encode(credentials.encode("utf-8"))
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache", "Authorization": f"Basic {authorization.decode('utf-8')}"}
        payload = dict(grant_type='client_credentials')
        response = self._send(endpoint='oauth2/token/', headers=headers, payload=dict(data=payload), authenticate=False)
        self._cache.store(self._ENS_SERVER, json.dumps(response)) if response.get('access_token', None) else print(f'Failed to authenticate:: {response}')

    def send_message(self, payload: dict) -> dict:
        response = self.process(endpoint='notification/send/', payload=payload, method='POST')
        return response

    def process(self, endpoint: str, payload, method: str, headers: dict = None):
        _ = self.token_expire_handler()

        payload = dict(params=payload) if method == 'GET' else dict(json=payload)
        response = self._send(endpoint=f'{endpoint}', headers=headers, payload=payload, method=method, authenticate=True)
        return response

    def _encrypt_base_authentication_code(self):
        credential = f'{self._CLIENT_ID}:{self._CLIENT_SECRET}'
        auth_code = base64.b64encode(credential.encode('utf-8'))
        return auth_code

    def _send(self, endpoint: str, headers: dict = None, payload: dict = None, method: str = 'post', authenticate: bool = False):
        if headers is None: headers = dict()
        if payload is None: payload = dict()

        headers, data = {**headers}, None
        if authenticate:
            cache_values = json.loads(self._cache.retrieve(self._ENS_SERVER))
            token_type = cache_values.get('token_type', None)
            access_token = cache_values.get("access_token", None)
            authorization = f'{token_type} {access_token}'
            headers = {
                **headers,
                'Authorization': authorization,
                'Content-Type': 'application/json'
            }

        print(f'Payload:: {payload}')
        print(f'Payload After:: {payload}')
        request = requests.Request(
            method=method,
            url=f'{self._ENS_SERVER}:{self._ENS_PORT}/{self._API_VERSION}/{endpoint}',
            **payload,
            headers=headers
        )
        try:
            prepared_request = request.prepare()
            print(f'Headers:: {prepared_request.headers}')
            print(f'Body:: {prepared_request.body}')
            print(f'Path:: {prepared_request.url}')
            session = requests.Session()
            session.verify = False
            session.trust_env = False
            response = session.send(prepared_request)
            print(f'ENS Response:: {response.text}')
            data = response.json()
        except json.JSONDecodeError as ex:
            print(f'ENS Exception:: {ex}')
            sentry_sdk.capture_exception(ex)
        return data
