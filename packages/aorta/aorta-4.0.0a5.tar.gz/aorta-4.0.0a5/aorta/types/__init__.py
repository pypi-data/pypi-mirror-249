# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeAlias
from typing import Union

from .command import Command
from .commandtype import CommandType
from .envelope import Envelope
from .event import Event
from .eventtype import EventType
from .imessagehandler import IMessageHandler
from .ipublisher import IPublisher
from .itransaction import ITransaction
from .itransport import ITransport
from .irunner import IRunner
from .message import Message
from .messagehandlertype import MessageHandlerType
from .messageheader import MessageHeader
from .messagemetadata import MessageMetadata
from .publishable import Publishable


__all__: list[str] = [
    'Command',
    'CommandType',
    'Envelope',
    'Event',
    'EventType',
    'IMessageHandler',
    'IPublisher',
    'IRunner',
    'ITransaction',
    'ITransport',
    'Message',
    'MessageHandlerType',
    'MessageHeader',
    'MessageMetadata',
    'Publishable',
]

MessageType: TypeAlias = Union[
    Command,
    Event
]