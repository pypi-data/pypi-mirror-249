import json
from typing import Any

from aio_pika import Message
from aio_pika.abc import AbstractChannel


class RabbitMQHandler:

    def __init__(
        self,
        channel: AbstractChannel,
    ):
        self.channel = channel

    async def publish(
        self,
        exchange: str,
        routing_key: str,
        body: Any,
    ):
        await (await self.channel.get_exchange(
            name=exchange,
            ensure=True,
        )).publish(
            message=Message(
                body=json.dumps(body).encode(),
                content_type='application/json'
            ),
            routing_key=routing_key,
            timeout=10 * 60,
        )
