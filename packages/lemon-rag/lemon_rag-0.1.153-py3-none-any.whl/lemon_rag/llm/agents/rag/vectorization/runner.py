from concurrent.futures import ThreadPoolExecutor
from typing import List

from lemon_rag.dependencies.data_access import data_access
from lemon_rag.dependencies.vector_access import vector_access, embed_sentence
from lemon_rag.lemon_runtime import models
from lemon_rag.llm.agents.rag.vectorization.content_extractor import Paragraph
from lemon_rag.utils import log

vectorization_pool = ThreadPoolExecutor(max_workers=8)


def parse_and_vectorize_document(file: models.KnowledgeBaseFileTab, paragraphs: List[Paragraph]):
    log.info("start parse the file, id=%s, filename=%s", file.id, file.origin_filename)
    paragraphs_records = data_access.create_paragraphs(file, paragraphs)


def start_parse_document(file: models.KnowledgeBaseFileTab, paragraphs: List[Paragraph]):
    parse_and_vectorize_document(file, paragraphs)
