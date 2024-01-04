# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any
from typing import Generator

import aorta
import fastapi
import fastapi.params
from fastapi.exceptions import RequestValidationError
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from fastapi.dependencies.utils import solve_dependencies

from aorta.types import IPublisher


class EndpointRunner(aorta.LocalRunner):
    __module__: str = 'aorta.ext.fastapi'
    request: fastapi.Request

    def __init__(
        self,
        request: fastapi.Request,
        publisher: IPublisher
    ):
        super().__init__(publisher=publisher)
        self.request = request

    async def handle(
        self,
        transaction: aorta.types.ITransaction,
        handler: aorta.types.IMessageHandler,
        envelope: aorta.types.Envelope[Any]
    ) -> tuple[bool, Any]:
            async with transaction:
                dependant = get_dependant(call=handler.run, path='/')
                dependant.dependencies.extend(self.get_injectors(handler))
                values, errors, *_ = await solve_dependencies(
                    request=self.request,
                    dependant=dependant,
                    # TODO: This assumes very specific internal FastAPI behaviors.
                    body=envelope, # type: ignore
                    dependency_overrides_provider=None
                )
                if errors:
                    raise RequestValidationError(errors)
                assert dependant.call is not None
                assert callable(dependant.call)
                
                # In some versions of FastAPI the envelope type is changed
                # to the generic type (TODO).
                values['envelope'] = envelope
                
                return await dependant.call(**values)

    def get_injectors(self, obj: Any) -> Generator[Dependant, None, None]:
        for attname, member in inspect.getmembers(obj):
            if not isinstance(member, fastapi.params.Depends):
                continue
            def setter(attname: str, dep: Any = member):
                async def f(dep: Any = dep) -> None:
                    setattr(obj, attname, dep)
                return f
            yield get_parameterless_sub_dependant(
                 depends=fastapi.Depends(setter(attname, member)),
                 path=str(self.request.url)
            )