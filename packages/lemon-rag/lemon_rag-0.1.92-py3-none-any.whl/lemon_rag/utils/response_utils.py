import asyncio
import queue
from queue import Queue
from typing import TypeVar

import sanic.response as sanic_response
from pydantic import BaseModel

T = TypeVar("T")

timeout = 10


class ErrorCode(BaseModel):
    status: int = 200
    code: int
    message: str


class ErrorCodes:
    ok = ErrorCode(code=20000, message="OK")
    invalid_json = ErrorCode(code=40001, message="请求JSON格式错误")
    username_existed = ErrorCode(code=40002, message="用户名已存在")
    invalid_username_or_password = ErrorCode(code=40003, message="用户名或密码不正确")
    unauthorized = ErrorCode(code=40100, message="未登录", status=401)
    invalid_token = ErrorCode(code=40101, message="无效的令牌", status=401)
    file_size_exceeded = ErrorCode(code=40102, message="文件尺寸超出限制，请将文件尺寸控制在3MB以内")
    empty_file = ErrorCode(code=40103, message="上传的文件为空，请检查后重新上传")
    file_count_exceeded = ErrorCode(code=40104, message="上传文件数量超过限制，每个知识库最多上传5个文件")
    file_extension_invalid = ErrorCode(code=40105, message="暂不支持该文件类型")
    permission_denied = ErrorCode(code=40300, message="你没有权限执行此操作")
    internal_server_error = ErrorCode(code=50000, message="服务器内部错误", status=500)
    knowledge_base_not_found = ErrorCode(code=40400, message="知识库不存在")


def response(code: ErrorCode = ErrorCodes.ok, data: T = ""):
    if isinstance(data, BaseModel):
        data = data.dict()
    return sanic_response.json({"code": code.code, "data": data, "message": code.message}, status=code.status)


def stream(q: Queue):
    async def stream_from_queue(res: sanic_response.StreamingHTTPResponse):
        total_sleep = 0
        while True:
            if total_sleep >= timeout:
                raise TimeoutError()
            try:
                data = q.get_nowait()
                if data == "end":
                    break
                await res.write(data)
                print(f"writen the data {data}")
            except queue.Empty:
                await asyncio.sleep(0.5)
                total_sleep += 0.5
        print("receive end")

    return sanic_response.stream(stream_from_queue)
