import time
from enum import Enum
from typing import List, Callable, Optional

from langchain_community.embeddings import OpenAIEmbeddings

from lemon_rag.lemon_runtime import models
from lemon_rag.utils import log


class EmbeddingModel(str, Enum):
    DEFAULT = "text-embedding-ada-002"


Embedding_F = Callable[[List[str]], List[List[float]]]


def get_embedding_function(metrics_name: str) -> Embedding_F:
    embeddings = [None]

    def init_embeddings_client():
        if embeddings[0]:
            return
        openai_config: Optional[models.OPENAIConfig] = models.OPENAIConfig.get_or_none()
        if not openai_config:
            raise ValueError("openai_config not found")
        embeddings[0] = OpenAIEmbeddings(openai_api_base=openai_config.base_url, openai_api_key=openai_config.api_key)

    def inner(text: List[str]) -> List[List[float]]:
        init_embeddings_client()
        start_time = time.time()
        client = embeddings[0]
        time_cost = time.time() - start_time
        embedding_key_len = [len(k) for k in text]
        log.info("[Embedding] /%s %.3fs embedding_key_len: %s", metrics_name, time_cost, embedding_key_len)
        return client.embed_documents(text)

    return inner
