import queue
from typing import Optional, Union, Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk

from lemon_rag.protocols.chat import ResponseChunk


class TextCallbackHandler(BaseCallbackHandler):
    def __init__(self, q: queue.Queue):
        self.q = q

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        self.q.put(ResponseChunk.add_text(token).json())
