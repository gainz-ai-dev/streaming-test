import aio_pika
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
from fastapi import FastAPI, Request

from gainz.settings import settings


class RabbitMQService:
    def __init__(self, channel_pool: Pool[AbstractChannel]):
        self.channel_pool = channel_pool

    async def declare_queue(self, queue_name: str):
        async with self.channel_pool.acquire() as channel:
            await channel.declare_queue(queue_name, durable=True)

    async def publish_message(self, queue_name: str, message: str):
        async with self.channel_pool.acquire() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name,
            )

    async def consume_messages(self, queue_name: str, callback):
        async with self.channel_pool.acquire() as channel:
            queue = await channel.declare_queue(queue_name, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await callback(message.body.decode())

# Dependency injection to get RabbitMQ channel pool from the FastAPI app state


def get_rmq_channel_pool(request: Request) -> Pool[AbstractChannel]:  # pragma: no cover
    return request.app.state.rmq_channel_pool
