


import json
import logging

logger = logging.getLogger(__name__)

async def order_status_listener(redis):
    pubsub = redis.pubsub()

    await pubsub.subscribe("order_status_changed")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        event = json.loads(message["data"])
        logger.info(f"Order status changed: = order_id={event['order_id']}, new_status={event['new_status']}, timestamp={event['timestamp']}")
