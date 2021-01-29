from typing import Optional

from fastapi import FastAPI
from fastapi import HTTPException

from db import User
from db import AllUsers
from db import Database


app = FastAPI(title="User API")
db = Database()

# TODO add response model to 404 error code response

@app.get("/users",
         response_description="Users",
         description="Get all Users from database",
         response_model=AllUsers,
         responses={
             200:{
                 "description": "Get users list",
                 "content": {
                     "application/json": {
                         "example": {"user_ids": [123, 234, 543]}
                     }
                 }
             },
             404:{"description": "The item was not found"}
         })
async def get_users():
    try:
        users = db.get_all_users()
    except ValueError as e:
        raise HTTPException(404, str(e))
    print(type(users))
    print(users)
    return users

@app.get("/user/{id}",
         response_description="User",
         description="Get User from database",
         response_model=User,
         responses={
             200:{
                 "description": "Get user",
                 "content": {
                     "application/json": {
                        "example": {
                             "id": 123,
                             "name": "John",
                             "age": 42
                           }
                     } 
                 }
             },
             404:{"description": "The User was not found"}
         })
async def get_user(id: int):
    try:
        user = db.get(id)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return user

@app.put(
    "/user",
    response_description="Added new User",
    response_model=User,
    responses={
             200:{
                 "description": "Get user",
                 "content": {
                     "application/json": {
                        "example": {
                             "id": 123,
                             "name": "John",
                             "age": 42
                           }
                     } 
                 }
             },
             404:{"description": "Couldn't create user."}
         }
)
async def add_user(user: User):
    try:
        user = db.add(user)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return user

@app.delete("/user/{id}",
            response_description="Result of deleting",
            responses={
                        200:{
                          "description": "Delete user",
                          "content": {
                              "application/json": {
                                 "example": {
                                      "result": "OK"
                                    }
                              } 
                          }
                        },
                        404:{"description": "Couldn't delete user."}
            }
)
async def delete_user(id: int):
    try:
        db.delete(id)
        return {"result": "OK"}
    except ValueError as e:
        raise HTTPException(404, str(e))
