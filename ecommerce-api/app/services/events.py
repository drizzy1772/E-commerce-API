
from datetime import datetime, timezone
import json

async def publish_order_status_changed(redis, order_id: int, new_status: str):
    event_json = {
        "order_id": order_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "new_status": new_status,
    }

    json_string = json.dumps(event_json)
    print(json_string)

    await redis.publish("order_status_changed", json_string)