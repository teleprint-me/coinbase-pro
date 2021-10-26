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
from abc import ABC
from abc import abstractproperty
from abc import abstractmethod

from requests import Response
from requests import Session
from requests.models import PreparedRequest


class AbstractAPI(ABC):
    @abstractproperty
    def version(self) -> int:
        pass

    @abstractproperty
    def url(self) -> str:
        pass

    @abstractmethod
    def endpoint(self, value: str) -> str:
        pass

    @abstractmethod
    def path(self, value: str) -> str:
        pass


class AbstractAuth(ABC):
    @abstractmethod
    def __init__(self,
                 key: str = None,
                 secret: str = None,
                 passphrase: str = None):

        pass

    @abstractmethod
    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        pass

    @abstractmethod
    def signature(self, message: str) -> bytes:
        pass

    @abstractmethod
    def header(self, timestamp: str, message: str) -> dict:
        pass


class AbstractMessenger(ABC):
    @abstractmethod
    def __init__(self, api: AbstractAPI = None, auth: AbstractAuth = None):
        pass

    @abstractproperty
    def api(self) -> AbstractAPI:
        pass

    @abstractproperty
    def auth(self) -> AbstractAuth:
        pass

    @abstractproperty
    def session(self) -> Session:
        pass

    @abstractproperty
    def timeout(self) -> int:
        pass

    @abstractmethod
    def get(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def post(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def put(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def delete(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def page(self, endpoint: str, data: dict = None) -> list:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class AbstractSubscriber(ABC):
    @abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass

    @abstractproperty
    def messenger(self) -> AbstractMessenger:
        pass

    @abstractmethod
    def error(self, response: Response) -> bool:
        pass


class AbstractClient(ABC):
    @abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass
