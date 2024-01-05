from dataclasses import dataclass
from typing import TypeAlias

from aio_pika import ExchangeType


QueueName: TypeAlias = str
ExchangeName: TypeAlias = str


@dataclass
class RabbitMQExchange:
    name: str
    type: ExchangeType
    durable: bool
    auto_delete: bool


@dataclass
class RabbitMQQueue:
    name: str
    auto_delete: bool
    durable: bool


@dataclass
class RabbitMQConfig:
    exchanges: list[RabbitMQExchange]
    queues: list[RabbitMQQueue]
    bindings: dict[QueueName, list[ExchangeName]]
