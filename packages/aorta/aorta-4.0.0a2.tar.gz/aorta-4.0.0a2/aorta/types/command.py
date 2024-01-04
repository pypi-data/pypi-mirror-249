# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import pydantic

from .commandtype import CommandType
from .envelope import Envelope


T = TypeVar('T', bound='Command')


class Command(pydantic.BaseModel, metaclass=CommandType):
    __envelope__: type[Envelope[Any]]

    def envelope(
        self,
        correlation_id: str | None = None,
        audience: set[str] | None = None
    ) -> Envelope[Any]:
        return self.__envelope__.model_validate({
            'apiVersion': getattr(self, '__version__', 'v1'),
            'kind': type(self).__name__,
            'type': 'unimatrixone.io/command',
            'metadata': {
                'audience': audience or set(),
                'correlationId': correlation_id
            },
            'spec': self.model_dump()
        })