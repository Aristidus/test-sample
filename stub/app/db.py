from typing import List, Optional, Union, NoReturn
import random
from pydantic import BaseModel
from pydantic import Field

# TODO id field must be unique!
class User(BaseModel):
    id: int = Field(..., title="Id", description="Id of the User")
    name: str = Field(..., title="Name", description="Name of the User", max_length=50)
    age: int = Field(..., title="Age", description="Age of the User")

class AllUsers(BaseModel):
    user_ids: List

class Database:
    def __init__(self):
        self._items: List[User] = [
            {
            "id": 123,
            "name": "John",
            "age": 42
            },
            {
            "id": 234,
            "name": "Mike",
            "age": 35
            },
            {
            "id": 543,
            "name": "Antony",
            "age": 25
            }
        ]

    def get(self, id: int) -> User:
        result_found = False
        for item in self._items:
            if item["id"] == id:
                result_found = True
                return item
        if not result_found:
            raise ValueError(f"User with id: {id} doesn't exist.")

    def get_all_users(self) -> AllUsers:
        ids = []
        for item in self._items:
            ids.append(item["id"])
            print(ids)
        return AllUsers(user_ids=ids)

    def add(self, user: User) -> User:
        result = self._items.append(dict(user))
        return user

    def delete(self, id: int) -> Union[NoReturn, None]:
        result_found = False
        for i, item in enumerate(self._items):
            if item["id"] == id:
                result_found = True
                del self._items[i]
        if not result_found:
            raise ValueError("User with id: {id} doesn't exist.")