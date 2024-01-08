# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable

from .types import Envelope
from .types import IPublisher
from .types import ITransaction
from .types import ITransport
from .transaction import Transaction


class MessagePublisher:
    __module__: str = 'aorta'
    transport: ITransport
    transaction_factory: Callable[[IPublisher], ITransaction]

    def __init__(
        self,
        transport: ITransport,
        transaction_factory: Callable[[IPublisher], ITransaction] | None = None
    ):
        self.transport = transport
        self.transaction_factory = transaction_factory or Transaction

    def begin(self) -> ITransaction:
        return self.transaction_factory(self)
    
    async def send(self, messages: list[Envelope[Any]], is_retry: bool = False) -> None:
        return await self.transport.send(messages, is_retry=is_retry)