import json


def marshal(v) -> str:
    return json.dumps(v)


def unmarshal(data: str):
    return json.loads(data)


def is_json(data: str) -> bool:
    try:
        marshal(data)
    except:
        return False
    else:
        return True
