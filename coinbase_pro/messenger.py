# coinbase-pro - A Python API Adapter for Coinbase Pro and Coinbase Exchange
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from coinbase_pro import __agent__
from coinbase_pro import __source__
from coinbase_pro import __version__
from coinbase_pro import __limit__

from coinbase_pro.abstract import AbstractAPI
from coinbase_pro.abstract import AbstractAuth
from coinbase_pro.abstract import AbstractMessenger
from coinbase_pro.abstract import AbstractSubscriber

from dataclasses import dataclass

from requests import Session
from requests import Response
from requests.auth import AuthBase
from requests.models import PreparedRequest

from time import time
from time import sleep

import base64
import hmac
import hashlib


@dataclass
class API(AbstractAPI):
    url: str = 'https://api.pro.coinbase.com'

    @property
    def version(self) -> int:
        return 1

    def endpoint(self, value: str) -> str:
        return f'/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Auth(AbstractAuth, AuthBase):
    def __init__(self,
                 key: str = None,
                 secret: str = None,
                 passphrase: str = None):

        self.__key = key if key else ''
        self.__secret = secret if secret else ''
        self.__passphrase = passphrase if passphrase else ''

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = str(time())
        body = str() if not request.body else request.body.decode('utf-8')
        message = f'{timestamp}{request.method.upper()}{request.path_url}{body}'
        header = self.header(timestamp, message)
        request.headers.update(header)
        return request

    def signature(self, message: str) -> bytes:
        key = base64.b64decode(self.__secret)
        msg = message.encode('ascii')
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode('utf-8')

    def header(self, timestamp: str, message: str) -> dict:
        return {
            'Content-Type': 'application/json',
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.__key,
            'CB-ACCESS-SIGN': self.signature(message),
            'CB-ACCESS-PASSPHRASE': self.__passphrase
        }


class Messenger(AbstractMessenger):
    def __init__(self, api: AbstractAPI = None, auth: AbstractAuth = None):
        self.__api: AbstractAPI = api if api else API()
        self.__auth: AbstractAuth = auth
        self.__session: Session = Session()

    @property
    def api(self) -> AbstractAPI:
        return self.__api

    @property
    def auth(self) -> AbstractAuth:
        return self.__auth

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def timeout(self) -> int:
        return 30

    def get(self, endpoint: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.get(
            self.api.path(endpoint),
            params=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def post(self, endpoint: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.post(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def put(self, endpoint: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.put(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def delete(self, endpoint: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.delete(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def page(self, endpoint: str, data: dict = None) -> list:
        responses = []
        if not data:
            data = {'limit': 20}
        while True:
            response = self.get(endpoint, data)
            if 200 != response.status_code:
                return [response]
            if not response.json():
                break
            responses.append(response)
            if not response.headers.get('CB-AFTER'):
                break
            data['after'] = response.headers.get('CB-AFTER')
        return responses

    def close(self):
        self.session.close()


class Subscriber(AbstractSubscriber):
    def __init__(self, messenger: AbstractMessenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def error(self, response: Response) -> bool:
        return 200 != response.status_code
