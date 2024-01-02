from functools import partial
from typing import Optional, List

from pydantic import BaseModel
from pymilvus import Connections, Collection, FieldSchema, DataType, CollectionSchema

from lemon_rag.lemon_runtime import models
from lemon_rag.llm.client.base_client import get_embedding_function

default_index_schema = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}

embed_sentence = get_embedding_function("embed_knowledge_base_sentence")


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

        milvus_token: Optional[models.VectorStoreConfig] = models.VectorStoreConfig.select().get_or_none()
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
                    FieldSchema(name="id", dtype=DataType.INT32, is_primary=True),
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
        self.knowledge_base_collection.insert([
            {
                "id": sentence_record.id,
                "raw_content": sentence_record.raw_content,
                "doc_name": sentence_record.paragraph.file.filename,
                "doc_id": sentence_record.paragraph.file.id,
                "vector": vector
            }
        ])


vector_access = VectorAccess()
