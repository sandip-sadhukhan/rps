from uuid import uuid4


def get_id():
    return str(uuid4())[:6]


def send_message(data):
    return {
        "type": "send_message",
        "data": data
    }
