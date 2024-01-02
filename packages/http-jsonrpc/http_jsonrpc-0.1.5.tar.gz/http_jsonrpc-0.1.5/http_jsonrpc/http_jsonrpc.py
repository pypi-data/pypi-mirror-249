import requests
import json

from functools import partial
from base64 import b64encode

class HttpJsonRpc(object):
    def __init__(self, endpoint, username=None, password=None, verify=False):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.verify = verify

    def send_message(self, method, headers=None, expect_reply=True, **params):
        headers = headers or {}
        if self.username and self.password:
            headers["Authorization"] = f'Basic {b64encode(bytes(f"{self.username}:{self.password}", "utf8")).decode("utf8")}'
        body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        response = requests.post(self.endpoint, json=body, headers=headers, verify=self.verify)

        if expect_reply:
            content = json.loads(response.content)
            if "result" in content.keys():
                return content["result"]
            else:
                if "error" in content.keys():
                    raise JsonRpcError(**json.loads(response.content)["error"])
                raise JsonRpcError("Unknown error:", response.content)

    def __getattr__(self, name):
        return partial(self.send_message, name)


class JsonRpcError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f'({self.code}) {self.message}'