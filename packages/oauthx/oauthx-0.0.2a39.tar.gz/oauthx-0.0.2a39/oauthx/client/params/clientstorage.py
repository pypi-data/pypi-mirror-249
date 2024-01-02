# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated
from typing import TypeAlias

import fastapi

from oauthx.client.protocols import ClientStorageType


__all__: list[str] = ['ClientStorage']


def get(request: fastapi.Request) -> ClientStorageType:
    return getattr(request.state, 'oauth_client_storage')


ClientStorage: TypeAlias  = Annotated[ClientStorageType, fastapi.Depends(get)]