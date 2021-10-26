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
import requests
import typing

__agent__: str = 'coinbase-pro'
__source__: str = 'https://github.com/teleprint-me/coinbase-pro'
__version__: str = '1.1.0'
__limit__: float = 1 / 3.5

List = typing.TypeVar('List', list, list[dict])
Dict = typing.TypeVar('Dict', dict, List)
Response = typing.TypeVar('Response', requests.Response, list[requests.Response])
