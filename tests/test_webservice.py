import requests as rq
import schemathesis
import pytest

schema = schemathesis.from_uri("http://localhost/openapi.json")

def test_get_all_users(api):
    response = api.get_all_users()
    assert type(response) == list
    assert response == [123, 234, 543]

def test_get_user(api):
    response = api.get_user(123)

    id = response["id"]
    name = response["name"]
    age = response["age"]
    assert type(id) == int and id == 123
    assert type(name) == str and name == "John"
    assert type(age) == int and age == 42

@pytest.mark.parametrize("data",
                    [
                        {
                            "id": 56465,
                            "name": "Kek",
                            "age": 32
                        },
                        {
                            "id": 3543,
                            "name": "Keklol Петрович",
                            "age": 150
                        }
                    ]
)
def test_create_user(api, data):
    response = api.add_user(data)
    assert response == data

    read_user_again = api.get_user(data["id"])
    assert read_user_again == data

@pytest.mark.parametrize("id", [56465, 3543])
def test_delete_user(api, id):
    response = api.delete_user(id)
    assert response == "OK"

    read_user_again = api.get_user(id)
    assert read_user_again["code"] == 404
    assert read_user_again["result"]["detail"] == f"User with id: {id} doesn't exist."

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
