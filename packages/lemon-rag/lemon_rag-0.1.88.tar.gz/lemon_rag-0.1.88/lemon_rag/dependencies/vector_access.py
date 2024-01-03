import time
from functools import partial
from typing import Optional, List, Union, Dict

from pydantic import BaseModel
from pymilvus import Connections, Collection, FieldSchema, DataType, CollectionSchema, Hit

from lemon_rag.lemon_runtime import models
from lemon_rag.llm.client.base_client import get_embedding_function
from lemon_rag.utils import log

default_index_schema = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}

embed_sentence = get_embedding_function("embed_knowledge_base_sentence")


class DocSearchRes(BaseModel):
    doc_id: str
    id: str


class VectorAccess(BaseModel):
    connections: Optional[Connections] = None
    knowledge_base_collection: Optional[Collection] = None
    initialized: bool = False
    init_msg: str = ""

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _init(self):
        if self.initialized:
            if self.init_msg:
                raise ValueError(f"milvus init failed for {self.init_msg}")
            return

        milvus_token: Optional[models.VectorStoreConfig] = models.VectorStoreConfig.get_or_none()
        if not milvus_token:
            self.initialized = True
            self.init_msg = "no milvus config found"
            raise ValueError("no milvus config found")
        connections = Connections()
        connections.connect("default", uri=milvus_token.uri, token=milvus_token.token)
        self.connections = connections
        self._init_collections()
        self.initialized = True

    def _init_collections(self):
        self.knowledge_base_collection = Collection(
            "data_model_overview",
            schema=CollectionSchema(
                [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
                    FieldSchema(name="raw_content", dtype=DataType.VARCHAR, max_length=2048),
                    FieldSchema(name="doc_name", dtype=DataType.VARCHAR, max_length=256),
                    FieldSchema(name="doc_id", dtype=DataType.INT32),
                    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1536),
                ]
            ))
        if not self.knowledge_base_collection.has_index():
            self.knowledge_base_collection.create_index("vector", default_index_schema)
        self.knowledge_base_collection.load()

    def save_sentence(self, sentence_record: models.KnowledgeSentence, vector: List[float]) -> None:
        self._init()

        self.knowledge_base_collection.insert([
            {
                "id": sentence_record.id,
                "raw_content": sentence_record.raw_content,
                "doc_name": sentence_record.paragraph.file.filename,
                "doc_id": sentence_record.paragraph.file.id,
                "vector": vector
            }
        ])

    def find_sentence(self, keywords: Union[List[str], str], doc_id_list: List[int], k: int = 5) -> List[DocSearchRes]:
        self._init()

        if not doc_id_list:
            return []
        start_time = time.time()
        if isinstance(keywords, str):
            keywords = [keywords]
        vectors = embed_sentence(keywords)

        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        expr = "doc_id in {}".format(doc_id_list)
        search_res = self.knowledge_base_collection.search(
            vectors, "vector", search_params, k, expr, None, ["id", "doc_id"]
        )
        res: List[Hit] = [hit for hits in search_res for hit in hits]
        res.sort(key=lambda h: h.score)  # distance, less is better
        res = res[:25]
        log.info(
            "[VectorAccess] /search_data_model_names %.3fs result=%s",
            time.time() - start_time,
            [f"[{hit.get('table_name')}, {hit.score:.3f}]" for hit in res]
        )
        return [DocSearchRes(**h.fields) for h in res]


vector_access = VectorAccess()
