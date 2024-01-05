from contextlib import asynccontextmanager
from typing import AsyncIterator

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustChannel, AbstractRobustConnection

from rmq_handler.configuration.config import RabbitMQConfig, RabbitMQExchange, RabbitMQQueue, ExchangeName, QueueName
from rmq_handler.handlers.publisher import RabbitMQHandler


class RabbitMQChannelHandler:
    _connection: AbstractRobustConnection | None = None

    @classmethod
    async def get_rabbit_mq(cls) -> AsyncIterator[RabbitMQHandler]:
        async with cls._get_channel() as channel:
            yield RabbitMQHandler(
                channel=channel,
            )

    @classmethod
    async def configure(
        cls,
        config: RabbitMQConfig,
        host: str,
        port: int,
        login: str,
        password: str,
    ):
        cls._connection = await aio_pika.connect_robust(
            host=host,
            port=port,
            login=login,
            password=password,
        )
        async with cls._get_channel() as channel:
            await cls._declare_exchanges(
                channel=channel,
                exchanges=config.exchanges,
            )
            await cls._declare_queues(
                channel=channel,
                queues=config.queues,
                bindings=config.bindings,
            )

    @classmethod
    @asynccontextmanager
    async def _get_channel(cls) -> AsyncIterator[AbstractRobustChannel]:
        if not cls._connection:
            raise ValueError("The connection isn't configured to the RabbitMQ.")
        connection = await cls._connection.channel()
        try:
            yield connection  # type: ignore
        finally:
            await connection.close()

    @classmethod
    async def _declare_exchanges(
        cls,
        channel: AbstractRobustChannel,
        exchanges: list[RabbitMQExchange],
    ):
        for exchange in exchanges:
            await channel.declare_exchange(
                name=exchange.name,
                type=exchange.type,
                auto_delete=exchange.auto_delete,
                durable=exchange.durable,
            )

    @classmethod
    async def _declare_queues(
        cls,
        channel: AbstractChannel,
        queues: list[RabbitMQQueue],
        bindings: dict[QueueName, list[ExchangeName]],
    ):
        for queue_data in queues:
            queue = await channel.declare_queue(
                name=queue_data.name,
                auto_delete=queue_data.auto_delete,
                durable=queue_data.durable,
            )
            for exchange in bindings.get(queue_data.name, ()):
                await queue.bind(exchange)
