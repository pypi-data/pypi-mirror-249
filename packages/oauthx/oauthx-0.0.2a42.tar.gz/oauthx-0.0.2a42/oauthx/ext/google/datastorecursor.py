# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import datetime
import functools
from typing import cast
from typing import Any
from typing import AsyncIterator
from typing import Generic
from typing import Iterable
from typing import Mapping
from typing import TypeVar

import pydantic
from canonical.exceptions import DoesNotExist
from canonical.exceptions import MultipleObjectsReturned
from google.cloud.datastore import Client
from google.cloud.datastore.query import PropertyFilter
from oauthx.ext.google.types import IDatastoreCursor
from oauthx.ext.google.types import IDatastoreQuery
from .types import IDatastoreEntity


T = TypeVar('T', bound=pydantic.BaseModel)


class DatastoreCursor(Generic[T]):
    _client: Client
    _filters: Iterable[tuple[str, str, int | str | datetime.datetime]]
    _kind: str
    _limit: int | None
    _loop: asyncio.AbstractEventLoop
    _model: type[T]
    _sort: list[str]

    def __init__(
        self,
        kind: str,
        model: type[T],
        client: Client,
        filters: Iterable[tuple[str, str, int | str | datetime.datetime]] | None = None,
        sort: Iterable[str] | None = None,
        page_size: int = 1000,
        limit: int | None = None
    ):
        self._client = client
        self._filters = filters or []
        self._kind = kind
        self._limit = limit
        self._loop = asyncio.get_running_loop()
        self._model = model
        self._page_size = page_size
        self._sort = list(sort or [])

    def model_factory(self, entity: Mapping[str, Any] | IDatastoreEntity) -> T:
        return self._model.model_validate(entity)

    async def all(self) -> AsyncIterator[T]:
        cursor: bytes | None = None
        while True:
            c = await self.run_query(limit=self._page_size, page=cursor)
            objects = list(c)
            if not objects:
                break
            for entity in objects:
                yield self.model_factory(dict(entity))
            if not c.next_page_token:
                break
            cursor = c.next_page_token

    async def first(self) -> T | None:
        c = await self.run_query(limit=1)
        objects = list(c)
        if not objects:
            return None
        return self.model_factory(dict(objects[0]))

    async def one(self) -> T:
        c = await self.run_query(limit=2)
        objects = list(c)
        if len(objects) > 1:
            raise MultipleObjectsReturned
        if not objects:
            raise DoesNotExist
        return self.model_factory(objects[0])

    async def run_query(self, limit: int | None = None, page: bytes | None = None) -> IDatastoreCursor:
        q = cast(IDatastoreQuery, self._client.query(kind=self._kind)) # type: ignore
        for filter in self._filters:
            q.add_filter(filter=PropertyFilter(*filter)) # type: ignore
        if self._sort:
            q.order = self._sort
        f = functools.partial(q.fetch, start_cursor=page, limit=limit)
        return await self._loop.run_in_executor(None, f) # type: ignore