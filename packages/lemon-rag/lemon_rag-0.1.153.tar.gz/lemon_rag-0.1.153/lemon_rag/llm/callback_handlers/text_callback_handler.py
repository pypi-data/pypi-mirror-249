import queue
import traceback
from typing import Optional, Any, Dict, List
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from lemon_rag.protocols.chat import ResponseChunk
from lemon_rag.utils import log


class TextCallbackHandler(BaseCallbackHandler):

    def __init__(self, q: queue.Queue, session_id: int, msg_id: int):
        self.q = q
        self.session_id = session_id
        self.msg_id = msg_id
        self.value = ""
        self.batch: int = 4
        log.info("callback initialized")

    @property
    def always_verbose(self) -> bool:
        return True

    def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        log.info("llm start")

    def on_llm_new_token(
            self,
            token: str,
            *args,
            **kwargs: Any,
    ) -> Any:
        if not token:
            log.info("llm new token is empty [%s]", token)
            return
        self.value += token
        if len(self.value) % self.batch == 0:

            try:
                log.info("llm new token: %s", token)
                self.q.put(ResponseChunk.add_text(self.session_id, self.msg_id, self.value).json())
            except:
                log.info(traceback.format_exc())
            self.value = ""

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        if self.value:
            self.q.put(ResponseChunk.add_text(self.session_id, self.msg_id, self.value).json())
        self.value = ""