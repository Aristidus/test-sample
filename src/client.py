import logging
import sys
from json import JSONDecodeError

import requests 

from src.config import Configuration

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s = %(levelname)s - %(message)s")
log = logging.getLogger()

class APIError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Status code: {self.code}, {self.message}."

class Client(object):
    def __init__(self, config: Configuration):
        self.endpoint = config.endpoint

    def _make_request(self, http_method, api_method, **params):
        headers = {}
        headers.update(params.pop("headers", {}))
        log.info(f"Making {http_method} request of API method: {api_method}, with params: {params}")
        result = requests.request(http_method,
                                  f"{self.endpoint.rstrip('/')}/{api_method.lstrip('/')}",
                                  headers=headers,
                                  **params)
        if result.status_code == 200:
            log.info(f"Status code: {result.status_code}, result: {result}")
            return result.json()
        else:
            try:
                error_code = result.status_code
                description = result.json()
                log.info(f"Status code: {error_code}, result: {result}")
                return {"code": error_code, "result": description}
            except JSONDecodeError:
                error_code = result.status_code
                error_message = "API request error."
                raise APIError(code=error_code, message=error_message)

    def get_all_users(self) -> list:
        log.info(f"Get list of all users")
        result = self._make_request("get", "users")
        users = result["user_ids"]
        return users

    def get_user(self, id: int) -> dict:
        log.info(f"Get user information with id: {id}")
        result = self._make_request("get", f"user/{id}")
        return result

    def add_user(self, data: dict) -> dict:
        log.info(f"Addt user data: {data}")
        result = self._make_request("put", f"user/", json=data)
        return result

    def delete_user(self, id: int):
        log.info(f"Delete user with id: {id}")
        result = self._make_request("delete", f"user/{id}")
        return result["result"]


