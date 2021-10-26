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
from time import sleep

import base64
import hashlib
import hmac
import json


def get_message() -> dict:
    return {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }


class Token(object):
    def __init__(self, key: str, secret: str, passphrase: str):
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase

    def __call__(self) -> dict:
        timestamp = str(time())
        signature = self.signature(timestamp)
        return self.header(timestamp, signature)

    def signature(self, timestamp: str) -> bytes:
        key = base64.b64decode(self.__secret)
        msg = f'{timestamp}GET/users/self/verify'.encode('ascii')
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode('utf-8')

    def header(self, timestamp: str, signature: bytes) -> dict:
        return {
            'signature': signature,
            'key': self.__key,
            'passphrase': self.__passphrase,
            'timestamp': timestamp
        }


@dataclass
class Stream(object):
    auth: Token = None
    url: str = 'wss://ws-feed.pro.coinbase.com'
    trace: bool = False
    timeout: int = 30
    socket: WebSocket = None

    @property
    def connected(self) -> bool:
        return False if not self.socket else self.socket.connected

    def connect(self) -> bool:
        header = None if not self.auth else self.auth()
        enableTrace(self.trace)
        if header:
            self.socket = create_connection(url=self.url, header=header)
        else:
            self.socket = create_connection(url=self.url)
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

    def ping(self) -> None:
        payload = 'keepalive'
        while self.connected:
            try:
                if self.trace:
                    print(f'[Ping] {payload} [Timeout] {self.timeout}s')
                self.socket.ping(payload)
                sleep(self.timeout)
            except (KeyboardInterrupt,):
                break

    def disconnect(self) -> bool:
        if self.connected:
            self.socket.close()
        return not self.connected
