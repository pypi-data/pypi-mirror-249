import time
from typing import Tuple
import requests

from . import urandom as urandom
from . import uquery
from . import uhmac
from . import ujson


class HttpStatusError(Exception):
    pass


class CodeError(Exception):
    def __init__(self, code: str, subcode: str):
        super().__init__()
        self.code = code
        self.subcode = subcode


class Client:
    def __init__(self, access_key: str, access_secret: str, endpoint: str):
        self._access_key = access_key
        self._access_secret = access_secret
        self._endpoint = endpoint

    def send_get_requests(self, path: str, query: dict) -> Tuple[dict, requests.Response]:
        timestamp = str(int(time.time()))
        n = urandom.generate_unique_number(18)

        query["xaccesskey"] = self._access_key
        query["xn"] = n
        query["xtimestamp"] = timestamp
        query["xrunmode"] = "release"

        query_str = uquery.get_query(query)

        sign_text = f"GET\n{self._access_key}\n{timestamp}\n{n}\n{path}\n{query_str}\n"
        sign = uhmac.string_calculate_hmac(self._access_secret, sign_text)

        query["xsign"] = sign
        query_str = uquery.get_query(query)
        url = f"{self._endpoint}{path}?{query_str}"

        resp = requests.get(url)

        if resp.status_code != 200:
            raise HttpStatusError

        data: dict = ujson.unmarshal(resp.text)
        code = data.get("code", "SUCCESS")
        subcode = data.get("subcode", "SUCCESS")

        if code != "SUCCESS":
            raise CodeError(code, subcode)

        return data, resp

    def send_post_requests(self, data: dict, path: str) -> Tuple[dict, requests.Response]:
        timestamp = str(int(time.time()))
        n = urandom.generate_unique_number(18)

        body = ujson.marshal(data)

        sign_text = f"POST\n{self._access_key}\n{timestamp}\n{n}\n{path}\n{body}\n"
        sign = uhmac.string_calculate_hmac(self._access_secret, sign_text)

        headers = {
            "Content-Type": "application/json",
            "X-AccessKey": self._access_key,
            "X-N": n,
            "X-Timestamp": timestamp,
            "X-RunMode": "release",
            "X-Sign": sign,
        }

        url = f"{self._endpoint}{path}"
        resp = requests.post(url, data=body, headers=headers)

        if resp.status_code != 200:
            raise HttpStatusError

        data: dict = ujson.unmarshal(resp.text)
        code = data.get("code", "SUCCESS")
        subcode = data.get("subcode", "SUCCESS")

        if code != "SUCCESS":
            raise CodeError(code, subcode)

        return data, resp
