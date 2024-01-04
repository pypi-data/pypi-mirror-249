# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import inspect
import socket
from collections import OrderedDict
from typing import Any
from typing import Awaitable
from typing import TypeVar
from typing import Callable

import httpx
import fastapi
from fastapi.concurrency import AsyncExitStack
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies


T = TypeVar('T')
R = TypeVar('R')
EMPTY = inspect._empty # type: ignore


def http(func: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(func)
    async def f(self: Any, *args: Any, **kwargs: Any) -> Any:
        client = kwargs.pop('http', None)
        if client is not None:
            return await func(self, client, *args, **kwargs)
        async with httpx.AsyncClient() as client:
            return await func(self, client, *args, **kwargs)
    return f


def insert_signature(
    func: Callable[..., Any],
):
    def decorator_factory(wrapper: Callable[..., Any]) -> Callable[..., Any]:
        f = inspect.signature(func)
        w = inspect.signature(wrapper)
        wrapper.__signature__ = f.replace( # type: ignore
            parameters=[
                *w.parameters.values(),
                *f.parameters.values()
            ]
        )
        return wrapper

    return decorator_factory


def set_signature_defaults(
    callable: Callable[..., Any],
    defaults: dict[str, Any]
) -> Callable[..., Any]:
    sig = inspect.signature(callable)
    params = OrderedDict(sig.parameters.items())
    for name, default in defaults.items():
        if name not in params:
            continue
        params[name] = inspect.Parameter(
            kind=params[name].kind,
            name=params[name].name,
            default=default,
            annotation=params[name].annotation
        )

    async def f(*args: Any, **kwargs: Any) -> Any:
        return await callable(*args, **kwargs)
    f.__signature__ = sig.replace(parameters=list(params.values())) # type: ignore
    return f


def random_port() -> int:
    """Return an integer indicating a port on the local system that
    is available.
    """
    with socket.socket() as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    return port


async def run(
    f: Callable[..., Awaitable[R] | R],
    *,
    scope: dict[str, Any] | None = None,
    **kwargs: Any
) -> R | None:
    async with AsyncExitStack() as stack:
        request: fastapi.Request = fastapi.Request({
            **(scope or {}),
            'fastapi_astack': stack,
            'headers': [],
            'query_string': None,
            'type': 'http',
        })

        dependant = get_dependant(call=f, path='/')
        values, errors, *_ = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=None,
            dependency_overrides_provider=None
        )
        kwargs = {**values, **kwargs}
        if errors:
            raise Exception(errors)
        assert callable(dependant.call)
        result = dependant.call(**kwargs)
        if inspect.isawaitable(result):
            result = await result
        return result


class class_property:
    __module__: str = 'oauthx.utils'

    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __get__(self, instance: Any, cls: Any) -> Any:
        return self.func(cls)
    

def merge_signatures(signatures: list[inspect.Signature]) -> inspect.Signature:
    """Merge signatures to that FastAPI can inject the dependencies."""
    params: dict[str, inspect.Parameter] = OrderedDict()
    for sig in signatures:
        for param in sig.parameters.values():
            if param.name in {'self', 'cls'}:
                continue
            if param.name.startswith('_'):
                continue
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                continue
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                continue
            params[param.name] = param

    return signatures[0].replace(
        parameters=list(sorted(params.values(), key=lambda p: (p.kind, p.default != inspect._empty))) # type: ignore
    )


def merged_call(func: Callable[..., Any], kwargs: Any) -> Any:
    sig = inspect.signature(func)
    return func(**{k: v for k, v in kwargs.items() if k in sig.parameters})