import json
from typing import Any

import requests

MESSAGE_SERVER_HOST = "http://localhost:17886/api/v1/messages"


def send_message(topic: str, message_body: Any):
    message = {
        "topic": topic,
        "data": json.dumps(message_body)
    }
    ret = requests.post(MESSAGE_SERVER_HOST, json.dumps(message))
    print(ret)
