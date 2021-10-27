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
from abc import ABC
from abc import abstractproperty
from abc import abstractmethod

from requests import Response
from requests import Session
from requests.models import PreparedRequest


class AbstractAPI(ABC):
    @abstractmethod
    def __init__(self, settings: dict = None):
        pass

    @abstractproperty
    def key(self) -> str:
        pass

    @abstractproperty
    def secret(self) -> str:
        pass

    @abstractproperty
    def passphrase(self) -> str:
        pass

    @abstractproperty
    def authority(self) -> str:
        pass

    @abstractproperty
    def version(self) -> int:
        pass

    @abstractmethod
    def path(self, value: str) -> str:
        pass

    @abstractmethod
    def url(self, value: str) -> str:
        pass


class AbstractAuth(ABC):
    @abstractmethod
    def __init__(self, api: AbstractAPI):
        pass

    @abstractmethod
    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        pass

    @abstractproperty
    def api(self) -> AbstractAPI:
        pass

    @abstractmethod
    def signature(self, message: str) -> bytes:
        pass

    @abstractmethod
    def header(self, timestamp: str, message: str) -> dict:
        pass


class AbstractMessenger(ABC):
    @abstractmethod
    def __init__(self, auth: AbstractAuth = None):
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
    def get(self, path: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def post(self, path: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def put(self, path: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def delete(self, path: str, data: dict = None) -> Response:
        pass

    @abstractmethod
    def page(self, path: str, data: dict = None) -> list:
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


class AbstractClient(ABC):
    @abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass
