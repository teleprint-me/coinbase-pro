# coinbase-pro - A Python Wrapper for Coinbase Pro and Coinbase Exchange
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
import base64
import hashlib
import hmac
from dataclasses import dataclass, field
from time import sleep, time

from requests import Response, Session
from requests.auth import AuthBase
from requests.models import PreparedRequest

from coinbase_pro import __agent__, __limit__, __source__, __version__
from coinbase_pro.abstract import (
    AbstractAPI,
    AbstractAuth,
    AbstractMessenger,
    AbstractSubscriber,
)


@dataclass
class API(AbstractAPI):
    settings: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return self.settings.get("key", "")

    @property
    def secret(self) -> str:
        return self.settings.get("secret", "")

    @property
    def passphrase(self) -> str:
        return self.settings.get("passphrase", "")

    @property
    def rest(self) -> str:
        return self.settings.get("rest", "https://api.pro.coinbase.com")

    @property
    def feed(self) -> str:
        return self.settings.get("feed", "wss://ws-feed.pro.coinbase.com")

    @property
    def version(self) -> int:
        return 1

    def path(self, value: str) -> str:
        return f'/{value.lstrip("/")}'

    def url(self, value: str) -> str:
        return f'{self.rest}/{self.path(value).lstrip("/")}'


class Auth(AbstractAuth, AuthBase):
    def __init__(self, api: API = None):
        self.__api = api if api else API()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = str(time())
        body = str() if not request.body else request.body.decode("utf-8")
        message = f"{timestamp}{request.method.upper()}{request.path_url}{body}"
        header = self.header(timestamp, message)
        request.headers.update(header)
        return request

    @property
    def api(self) -> API:
        return self.__api

    def signature(self, message: str) -> bytes:
        key = base64.b64decode(self.api.secret)
        msg = message.encode("ascii")
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode("utf-8")

    def header(self, timestamp: str, message: str) -> dict:
        return {
            "Content-Type": "application/json",
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-ACCESS-KEY": self.api.key,
            "CB-ACCESS-SIGN": self.signature(message),
            "CB-ACCESS-PASSPHRASE": self.api.passphrase,
        }


class Messenger(AbstractMessenger):
    def __init__(self, auth: Auth = None):
        self.__auth: AbstractAuth = auth if auth else Auth()
        self.__session: Session = Session()

    @property
    def auth(self) -> Auth:
        return self.__auth

    @property
    def api(self) -> API:
        return self.__auth.api

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def timeout(self) -> int:
        return 30

    def get(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.get(
            self.api.url(path), params=data, auth=self.auth, timeout=self.timeout
        )

    def post(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.post(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def put(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.put(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def delete(self, path: str, data: dict = None) -> Response:
        sleep(__limit__)
        return self.session.delete(
            self.api.url(path), json=data, auth=self.auth, timeout=self.timeout
        )

    def page(self, path: str, data: dict = None) -> list:
        responses = []
        if not data:
            data = {"limit": 20}
        while True:
            response = self.get(path, data)
            if 200 != response.status_code:
                return [response]
            if not response.json():
                break
            responses.append(response)
            if not response.headers.get("CB-AFTER"):
                break
            data["after"] = response.headers.get("CB-AFTER")
        return responses

    def close(self):
        self.session.close()


class Subscriber(AbstractSubscriber):
    def __init__(self, messenger: Messenger = None):
        self.__messenger = messenger if messenger else Messenger()

    @property
    def messenger(self) -> Messenger:
        return self.__messenger

    # NOTE: error is left here as a convenience method for plugs
    def error(self, response: Response) -> bool:
        return 200 != response.status_code
