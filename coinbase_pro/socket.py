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
from dataclasses import dataclass

from websocket import enableTrace
from websocket import create_connection
from websocket import WebSocket

from time import time

import base64
import hashlib
import hmac
import json


@dataclass
class WSS(object):
    def __init__(self, settings: dict = None):
        self.__settings = settings if settings else {
            'key': '',
            'secret': '',
            'passphrase': '',
            'authority': 'wss://ws-feed.pro.coinbase.com'
        }

    @property
    def key(self) -> str:
        return self.__settings['key']

    @property
    def secret(self) -> str:
        return self.__settings['secret']

    @property
    def passphrase(self) -> str:
        return self.__settings['passphrase']

    @property
    def url(self) -> str:
        return self.__settings['authority']

    @property
    def version(self) -> int:
        return 1


class Token(object):
    def __init__(self, wss: WSS = None):
        self.__wss = wss if wss else WSS()

    def __call__(self) -> dict:
        timestamp = str(time())
        signature = self.signature(timestamp)
        return self.header(timestamp, signature)

    @property
    def wss(self) -> WSS:
        return self.__wss

    def signature(self, timestamp: str) -> bytes:
        key = base64.b64decode(self.wss.secret)
        msg = f'{timestamp}GET/users/self/verify'.encode('ascii')
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode('utf-8')

    def header(self, timestamp: str, signature: bytes) -> dict:
        return {
            'signature': signature,
            'key': self.wss.key,
            'passphrase': self.wss.passphrase,
            'timestamp': timestamp
        }


class Stream(object):
    def __init__(self, token: Token = None):
        self.__token: Token = token if token else Token()
        self.__wss: WSS = self.__token.wss
        self.socket: WebSocket = None

    @property
    def token(self) -> Token:
        return self.__token

    @property
    def wss(self) -> WSS:
        return self.__wss

    @property
    def auth(self) -> bool:
        return self.wss.key and self.wss.secret and self.wss.passphrase

    @property
    def connected(self) -> bool:
        return False if not self.socket else self.socket.connected

    def connect(self, trace: bool = False) -> bool:
        enableTrace(trace)
        if self.auth:
            self.socket = create_connection(url=self.wss.url, header=self.token())
        else:
            self.socket = create_connection(url=self.wss.url)
        return self.connected

    def send(self, message: dict) -> None:
        if self.connected:
            self.socket.send(json.dumps(message))

    def receive(self) -> dict:
        if self.connected:
            payload = self.socket.recv()
            if payload:
                return json.loads(payload)
        return dict()

    def disconnect(self) -> bool:
        if self.connected:
            self.socket.close()
        return not self.connected


def get_message() -> dict:
    return {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }


def get_stream(settings: dict = None) -> Stream:
    return Stream(Token(WSS(settings)))
