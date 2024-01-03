import base64
from io import StringIO
from typing import List, Optional, Dict

from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route, handle_chat_auth
from lemon_rag.api.local import get_user
from lemon_rag.configs.api_config import runtime_config
from lemon_rag.dependencies.data_access import data_access, KnowledgeBasePermission
from lemon_rag.lemon_runtime import models, wrappers
from lemon_rag.llm.agents.rag.retrieval.retrive_knowledgebase import retrieve_related_paragraphs, RelatedSentence
from lemon_rag.llm.agents.rag.vectorization.content_extractor import TxtExtractor
from lemon_rag.llm.agents.rag.vectorization.runner import start_parse_document
from lemon_rag.protocols.chat import ChatRole, Session, KnowledgeBase
from lemon_rag.utils import log
from lemon_rag.utils.file_utils import get_file_hash
from lemon_rag.utils.response_utils import response, ErrorCodes


class ListSessionRequest(BaseModel):
    version: int


class ListSessionResponse(BaseModel):
    up_to_date: bool = False
    sessions: Optional[List[Session]] = None


@handle_chat_auth
@handle_request_with_pydantic(ListSessionRequest)
def list_session(req: ListSessionRequest):
    assistant_session, _ = data_access.get_or_create_session(get_user(), ChatRole.assistant)
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    return response(data=ListSessionResponse(sessions=[
        Session(**model_to_dict(assistant_session)),
        Session(**model_to_dict(notification_session))
    ]))


class GetNotificationCountRequest(BaseModel):
    version: int


class GetNotificationCountResponse(BaseModel):
    version: int
    unread_count: int


@handle_chat_auth
@handle_request_with_pydantic(GetNotificationCountRequest)
def get_notification_count(req: GetNotificationCountRequest):
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    sync_history: models.SyncHistoryTab = notification_session.sync_history.get()
    return response(data=GetNotificationCountResponse(
        version=notification_session.version,
        unread_count=(notification_session.last_msg_id or 0) - (sync_history.last_read_id or 0)
    ))


class ReadNotificationsRequest(BaseModel):
    msg_id: int


@handle_chat_auth
@handle_request_with_pydantic(ReadNotificationsRequest)
def read_notifications(req: ReadNotificationsRequest):
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    data_access.read_message(notification_session, msg_id=req.msg_id)
    return response()


class UploadFileRequest(BaseModel):
    file_content: str
    filename: str
    knowledge_base_id: int


class UploadFilesResponse(BaseModel):
    id: int
    filename: str
    origin_filename: str


def extract_extension(filename: str) -> str:
    return filename.split('.')[-1]


@handle_chat_auth
@handle_request_with_pydantic(UploadFileRequest)
def upload_knowledge_base_file(req: UploadFileRequest):
    file_content: bytes = base64.b64decode(req.file_content)
    file_size: int = len(file_content)
    extension = extract_extension(req.filename)
    # check file basic
    if file_size <= 0:
        return response(code=ErrorCodes.empty_file)
    if file_size >= runtime_config.max_file_bytes:
        return response(code=ErrorCodes.file_size_exceeded)
    if extension not in runtime_config.supported_file_types:
        return response(code=ErrorCodes.file_extension_invalid)

    # check kb existence
    kb = data_access.get_knowledge_base_by_id(req.knowledge_base_id)
    if not kb:
        log.info("knowledge base not found, id=%s", req.knowledge_base_id)
        return response(code=ErrorCodes.knowledge_base_not_found)

    # check access
    access = data_access.get_knowledge_base_access(get_user(), kb)
    if not access:
        log.info("no access found for the knowledge_base=%s", kb)
        return response(code=ErrorCodes.permission_denied)

    if not (access.permission & KnowledgeBasePermission.write):
        log.info(
            "the user has permission=%s, but permission=%s required",
            access.permission,
            KnowledgeBasePermission.write
        )
        return response(code=ErrorCodes.permission_denied)

    #
    if data_access.get_knowledge_base_file_count(kb) >= kb.max_files:
        return response(code=ErrorCodes.file_count_exceeded)

    # check hash
    file_hash = get_file_hash(file_content)
    if file := data_access.upload_file_by_hash(get_user(), file_hash, kb):
        return response(data=UploadFilesResponse(**model_to_dict(file)))

    oss_file = wrappers.file_system.create_file(file_content, file_hash)
    oss_file.save()
    log.info("upload file, filename=%s, uploaded path=%s", req.filename, oss_file.url)
    file = data_access.create_file(oss_file.url, extension, req.filename, file_size, file_hash, kb, get_user())

    #
    buf = StringIO(file_content.decode("utf-8"))
    paragraphs = TxtExtractor().extract_content(buf)
    log.info("extracted paragraphs count=%s from %s", len(paragraphs), req.filename)
    start_parse_document(file, paragraphs)
    return response(data=UploadFilesResponse(**model_to_dict(file)))


class FileProcessProgressRequest(BaseModel):
    file_id: int


class FileProcessProgressResponse(BaseModel):
    id: int
    total_parts: int
    vectorized_parts: int


@handle_chat_auth
@handle_request_with_pydantic(FileProcessProgressRequest)
def file_process_progress(request: FileProcessProgressRequest):
    file = data_access.get_file_by_id(request.file_id)
    if not file:
        return response(code=ErrorCodes.file_not_found)
    return response(data=FileProcessProgressResponse(**model_to_dict(file)))


class ListKnowledgeBasesRequest(BaseModel):
    version: int


class ListKnowledgeBasesResponse(BaseModel):
    knowledge_bases: List[KnowledgeBase]


@handle_chat_auth
@handle_request_with_pydantic(ListKnowledgeBasesRequest)
def list_knowledge_bases(req: ListKnowledgeBasesRequest):
    return response()


class SendMessageRequest(BaseModel):
    text: str
    session_id: int


@handle_chat_auth
@handle_request_with_pydantic(SendMessageRequest)
def send_message(request: SendMessageRequest):
    return response()


class RateMessageRequest(BaseModel):
    msg_id: int


@handle_chat_auth
@handle_request_with_pydantic(RateMessageRequest)
def rate_message(abc):
    response()


class RetrySendMessageRequest(BaseModel):
    msg_id: int


@handle_chat_auth
@handle_request_with_pydantic(RetrySendMessageRequest)
def retry_send_message():
    # 判断是否是最新一条消息，如果是则复用发送消息逻辑
    pass


class SearchKnowledgebaseRequest(BaseModel):
    query: str
    knowledgebase_id: int


@handle_chat_auth
@handle_request_with_pydantic(SearchKnowledgebaseRequest)
def search_knowledgebase(request: SearchKnowledgebaseRequest):
    knowledgebase = data_access.get_knowledge_base_by_id(request.knowledgebase_id)
    if not knowledgebase:
        return response(code=ErrorCodes.knowledge_base_not_found)
    file_ids = [link.file.id for link in knowledgebase.file_links]
    res: Dict[str, RelatedSentence] = retrieve_related_paragraphs(request.query, file_ids)
    return response(data=list(res.values()))


add_route("list_session", list_session)
add_route("get_notification_count", get_notification_count)
add_route("read_notifications", read_notifications)
add_route("upload_knowledge_base_file", upload_knowledge_base_file)
add_route("send_message", send_message)
add_route("rate_message", rate_message)
add_route("retry_send_message", retry_send_message)
add_route("list_knowledge_bases", list_knowledge_bases)
add_route("search_knowledgebase", search_knowledgebase)
add_route("file_process_progress", file_process_progress)
