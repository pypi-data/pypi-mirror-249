# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Union

from .commandhandler import CommandHandler
from .types import Command


class Ping(Command):
    message: str = 'Nice to meet you!'


class Pong(Command):
    message: str = 'Likewise!'


CommandType = Union[Ping, Pong]


class PingHandler(CommandHandler[CommandType]):

    async def handle(self, command: CommandType) -> Any:
        self.logger.debug("Pong (message: %s)", command.message)