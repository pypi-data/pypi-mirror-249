# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

import httpx
import pytest

import oauthx
from .types import AuthorizeFactory


@pytest.fixture(scope='function')
def client_credential() -> str:
    return bytes.hex(os.urandom(16))


@pytest.mark.asyncio
async def test_client_must_authenticate(
    http: httpx.AsyncClient,
    client: oauthx.Client,
    authorize_request: AuthorizeFactory
):
    _, params, state = await authorize_request(response_type='code')
    try:
        client.credential = bytes.hex(os.urandom(32))
        await client.authorization_code(params, state, http=http)
        assert False
    except oauthx.Error as exc:
        assert exc.error == 'invalid_client'