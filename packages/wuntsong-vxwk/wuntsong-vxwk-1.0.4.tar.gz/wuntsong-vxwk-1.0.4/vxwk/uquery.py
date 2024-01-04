import urllib.parse


def get_query(query: dict) -> str:
    target = sorted(query.items(), key=lambda x: x[0], reverse=False)
    return urllib.parse.urlencode(target)