import time
import uuid
from typing import Optional

import sanic.request
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route
from lemon_rag.core.executor_pool import submit_streaming_task
from lemon_rag.dependencies.data_access import data_access
from lemon_rag.lemon_runtime import models
from lemon_rag.utils import log
from lemon_rag.utils.password_match import hash_password
from lemon_rag.utils.response_utils import response, stream, ErrorCodes


def hello_world(request: sanic.request.Request):
    return response()


def hello_stream(request: sanic.request.Request):
    def generator():
        for line in ["aaaaa", "bbbbb", "ccccc", "ddddd"]:
            yield line
            time.sleep(1)

    queue = submit_streaming_task(generator())

    return stream(queue)


class RegisterRequest(BaseModel):
    username: str
    password: str
    mobile_number: str
    code: str


class RegisterResponse(BaseModel):
    id: int
    username: str
    nickname: str
    last_signin: str
    avatar: str


@handle_request_with_pydantic(RegisterRequest)
def register(req: RegisterRequest):
    existed_user: Optional[models.AuthUserTab] = models.AuthUserTab.get_or_none(username=req.username)
    if existed_user:
        log.info("[register] existed user, username=%s", req.username)
        return response(code=ErrorCodes.username_existed)

    user = models.AuthUserTab.create(**{
        "username": req.username,
        "password": hash_password(req.password)
    })
    data_access.init_account(user)
    return response(data=RegisterResponse(**model_to_dict(user)))


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    token: str
    create_at: int
    expire_at: int


@handle_request_with_pydantic(SignInRequest)
def sign_in(req: RegisterRequest):
    auth_user = models.AuthUserTab.get_or_none(username=req.username)
    if not auth_user:
        return response(code=ErrorCodes.invalid_username_or_password)

    if auth_user.password != hash_password(req.password):
        return response(code=ErrorCodes.invalid_username_or_password)

    token = data_access.generate_new_auth_token(auth_user)
    return response(data=SignInResponse(**model_to_dict(token)))


add_route("register", register)
add_route("sign_in", sign_in)
