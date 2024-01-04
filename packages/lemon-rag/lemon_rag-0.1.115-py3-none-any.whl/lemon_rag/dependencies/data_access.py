import time
import uuid
from enum import Enum
from typing import Tuple, Optional, List, Iterable

import peewee

from lemon_rag.lemon_runtime import models
from lemon_rag.llm.agents.rag.vectorization.content_extractor import Paragraph
from lemon_rag.protocols.chat import ChatRole, CardMessage, CardComponent, TextComponent, Session
from lemon_rag.utils import log


class KnowledgeBasePermission(int, Enum):
    read = 1
    write = 1 << 1
    read_write = read | write


class DataAccess:
    def generate_new_auth_token(self, auth_user: models.AuthUserTab) -> models.AppAuthTokenTab:
        token = uuid.uuid4().hex
        token = models.AppAuthTokenTab.create(**{
            "token": token,
            "user": auth_user,
            "created_at": int(time.time()),
            "expire_at": int(time.time()) + 60 * 60 * 24 * 100
        })
        return token

    def get_or_create_session(self, user: models.AuthUserTab, role: ChatRole) -> Tuple[models.SessionTab, bool]:
        title = "AI助手" if role == ChatRole.assistant else "通知中心"
        session, create = models.SessionTab.get_or_create(
            user=user,
            assistant_role=role,
            defaults={
                "created_at": int(time.time()),
                "topic": "",
                "title": title,
                "assistant_role": role,
                "last_msg_id": 0,
                "last_msg_ts": int(time.time())
            }
        )
        if create:
            models.SyncHistoryTab.create(**{
                "session": session,
                "last_read_id": 0,
                "last_read_ts": int(time.time())
            })
        return session, create

    def read_message(self, session: models.SessionTab, read_id: int) -> int:
        return models.SyncHistoryTab.update(
            **{"last_read_id": read_id, "last_read_ts": int(time.time())}
        ).where(models.SyncHistoryTab.session == session).execute()

    def init_account(self, user: models.AuthUserTab):
        kb = self.create_knowledge_base(
            user, "默认知识库", 100
        )
        log.info("created default knowledge base id=%s for the user=%s", kb, user)

        quota = models.UserQuotaTab.create(**{
            "auth_user": user,
            "request_per_min": 2,
            "request_per_day": 240,
            "request_per_month": 5000,
            "max_files": 100,
            "max_single_file_size": 1024 * 1024 * 5,
            "max_total_knowledge_size": 1025 * 1024 * 1024,
        })
        log.info("created default quota id=%s for the user=%s", quota, user)

    def create_knowledge_base(self, user: models.AuthUserTab, name: str, max_files: int) -> models.KnowledgeBaseTab:
        kb = models.KnowledgeBaseTab.create(**{
            "name": name,
            "owner": user,
            "max_files": max_files,
            "created_at": int(time.time())
        })
        models.KnowledgeBaseAccessTab.create(
            **{
                "permission": KnowledgeBasePermission.read_write,
                "create_at": int(time.time()),
                "user": user,
                "knowledge_base": kb,
                "creator": user
            },
        )
        return kb

    def get_knowledge_base_by_id(self, kb_id: int) -> Optional[models.KnowledgeBaseTab]:
        return models.KnowledgeBaseTab.get_or_none(kb_id)

    def upload_file_by_hash(self, user: models.AuthUserTab, hash_value: str, kb: models.KnowledgeBaseTab) -> Optional[
        models.KnowledgeBaseFileTab]:
        file: Optional[models.KnowledgeBaseFileTab] = models.KnowledgeBaseFileTab.get_or_none(content_hash=hash_value)
        if not file:
            return None
        models.FileUploadRecordTab.create(**{
            "upload_time": int(time.time()),
            "file": file,
            "uploader": user,
            "first_upload": False
        })
        models.KnowledgebaseFileLink.create(**{
            "file": file,
            "knowledgebase": kb
        })
        return file

    def get_file_by_id(self, file_id: int) -> Optional[models.KnowledgeBaseFileTab]:
        return models.KnowledgeBaseFileTab.get_or_none(file_id)

    def get_knowledge_base_access(
            self,
            user: models.AuthUserTab,
            kb: models.KnowledgeBaseTab
    ) -> Optional[models.KnowledgeBaseAccessTab]:
        try:
            return (
                models
                .KnowledgeBaseAccessTab
                .select()
                .where(
                    models.KnowledgeBaseAccessTab.knowledge_base == kb,
                    models.KnowledgeBaseAccessTab.user == user
                )
                .get()
            )
        except models.KnowledgeBaseAccessTab.DoesNotExist:
            return None

    def get_knowledge_base_file_count(self, kb: models.KnowledgeBaseTab) -> int:
        return kb.file_links.select(peewee.fn.Count(peewee.SQL("1"))).scalar()

    def create_file(
            self,
            filename: str,
            extension: str,
            origin_filename: str,
            file_size: int,
            content_hash: str,
            kb: models.KnowledgeBaseTab,
            user: models.AuthUserTab
    ) -> models.KnowledgeBaseFileTab:
        file = models.KnowledgeBaseFileTab.create(**{
            "filename": filename,
            "extension": extension,
            "origin_filename": origin_filename,
            "file_size": file_size,
            "total_parts": 0,
            "vectorized_parts": 0,
            "content_hash": content_hash
        })
        models.KnowledgebaseFileLink.create(**{
            "file": file,
            "knowledgebase": kb
        })
        models.FileUploadRecordTab.create(**{
            "upload_time": int(time.time()),
            "file": file,
            "uploader": user,
            "first_upload": True
        })
        return file

    def create_paragraphs(
            self,
            file: models.KnowledgeBaseFileTab,
            paragraphs: List[Paragraph]
    ) -> List[models.KnowledgeParagraph]:
        res = []
        sentence_count = sum([len(p.sentences) for p in paragraphs])
        for index, paragraph in enumerate(paragraphs):
            paragraph_record = models.KnowledgeParagraph.create(**{
                "raw_content": "".join(paragraph.sentences),
                "index": index,
                "context_content": "".join(paragraph.sentences),
                "total_sentences": len(paragraph.sentences),
                "file": file
            })
            res.append(paragraph_record)

            for s_index, sentence in enumerate(paragraph.sentences):
                models.KnowledgeSentence.create(**{
                    "index": s_index,
                    "raw_content": sentence,
                    "vectorized": False,
                    "paragraph": paragraph_record,
                    "file": file
                })
        file.total_parts = sentence_count
        file.vectorized_parts = 0
        file.save(only=["total_parts", "vectorized_parts"])
        return res

    def update_file_vectorized_count(self, file: models.KnowledgeBaseFileTab):
        file.vectorized_parts = models.KnowledgeSentence.select(peewee.fn.Count(peewee.SQL('1'))).where(
            models.KnowledgeSentence.file == file,
            models.KnowledgeSentence.vectorized == True
        ).scalar()
        file.save(only=["vectorized_parts"])

    def find_file_not_vectorized(self) -> Iterable[models.KnowledgeBaseFileTab]:
        return models.KnowledgeBaseFileTab.select().where(
            models.KnowledgeBaseFileTab.total_parts > 0,
            models.KnowledgeBaseFileTab.vectorized_parts == 0
        )

    def get_session_by_id(self, session_id: int) -> Optional[models.SessionTab]:
        return models.SessionTab.get_or_none(session_id)

    def get_msg_id(self, session_id: int) -> int:
        (models
         .SessionTab
         .update(**{
            "last_msg_id": models.SessionTab.last_msg_id + 1,
            "last_mst_ts": int(time.time())
        })
         .where(
            models.SessionTab.id == session_id
        )
         .execute())

        return list(
            models
            .SessionTab
            .select(
                models.SessionTab.last_msg_ts
            )
            .where(
                models.SessionTab.id == session_id
            ).limit(1)
        )[0].last_msg_id

    def create_message_and_response(
            self,
            user: models.AuthUserTab,
            session: models.SessionTab,
            content: str,
            client_ts: int
    ) -> Tuple[models.MessageTab, models.MessageTab]:
        user_msg_id = self.get_msg_id(session.id)
        user_message = models.MessageTab.create(**{
            "session": session,
            "msg_id": user_msg_id,
            "role": ChatRole.user,
            "is_system": False,
            "client_ts": client_ts,
            "server_ts": int(time.time()),
            "is_answer": False,
            "is_system_msg": False,
            "support_retry": True,
            "support_rating": True,
            "content": CardMessage(components=[TextComponent(id=0, data=content)]).json(),
            "text": content,
            "context_text": content,
            "version": 0,
            "user": user
        })
        ai_msg_id = self.get_msg_id(session.id)
        ai_message = models.MessageTab.create(**{
            "session": session,
            "msg_id": ai_msg_id,
            "role": ChatRole.assistant,
            "is_system": False,
            "client_ts": int(time.time()),
            "server_ts": int(time.time()),
            "is_answer": True,
            "question": user_message,
            "is_system_msg": False,
            "support_retry": True,
            "support_rating": True,
            "content": CardMessage(components=[]).json(),
            "text": "",
            "context_text": "",
            "version": 0,
            "user": user,
            "accepted": True
        })
        return user_message, ai_message

    def get_user_default_knowledgebase(self, user: models.AuthUserTab):
        return models.KnowledgeBaseTab.get_or_none(owner=user)


data_access = DataAccess()
