from typing import Optional, Union, Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk


class TextCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.value = ""

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        pass