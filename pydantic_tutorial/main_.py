from pathlib import Path

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI


# app = FastAPI()
#
#
# data = {
#     "email": "abc@gmail.ru",
#     "bio": "Bam bam bam, bam, bam bam bam bam",
#     "age": 12,
# }
#
# data_wo_age = {
#     "email": "abc@gmail.ru",
#     "bio": "Bam bam bam, bam, bam bam bam bam",
# }
#
# class UserSchema(BaseModel):
#     email: EmailStr
#     bio: str | None = Field(max_length=100)
#
#     model_config = ConfigDict(extra='forbid')
#
#
# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)
#
#
# users= []
#
# @app.post("/users")
# def add_user(user_: UserSchema):
#     users.append(user_)
#     return {"ok": True, "msg": "User is added"}
#
#
# @app.get("/users")
# def get_users() -> list[UserSchema]:
#     return users
#
#
# def func(data_: dict):
#     data_["age"] += 1
#
#
# user = UserAgeSchema(**data)
# user_wo_age = UserSchema(**data_wo_age)
# print(repr(user))
# print(repr(user_wo_age))





