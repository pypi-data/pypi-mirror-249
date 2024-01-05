"""
Patch the tiny-api-client decorators during testing
"""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA


import pytest
from unittest import mock

from typing import Any
from collections.abc import Generator, Callable


def _api_call(endpoint: str, **kwargs: Any) -> Any:
    """Placeholder function to patch when testing"""
    return None


# Patch the method decorators with a call to `_api_call`
def _method(route: str, **k: Any) -> Callable[[Callable], Callable]:
    return lambda fn: lambda self, *args, **_: fn(
        self, _api_call(route, **k), *args
    )


mock.patch('tiny_api_client.get', _method).start()
mock.patch('tiny_api_client.post', _method).start()
mock.patch('tiny_api_client.put', _method).start()
mock.patch('tiny_api_client.patch', _method).start()
mock.patch('tiny_api_client.delete', _method).start()


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    mock.patch.stopall()


@pytest.fixture()
def api_call() -> Generator[mock.Mock, None, None]:
    """A mock api call fixture to test api client classes"""
    with mock.patch(f"{__name__}._api_call") as p:
        yield p
