from concurrent.futures import ThreadPoolExecutor
from typing import List

from lemon_rag.dependencies.data_access import data_access
from lemon_rag.dependencies.vector_access import vector_access, embed_sentence
from lemon_rag.lemon_runtime import models
from lemon_rag.llm.agents.rag.content_extractor import Paragraph

vectorization_pool = ThreadPoolExecutor(max_workers=8)


def parse_and_vectorize_document(file: models.KnowledgeBaseFileTab, paragraphs: List[Paragraph]):
    paragraphs_records = data_access.create_paragraphs(file, paragraphs)
    for paragraph in paragraphs_records:
        for sentence in paragraph.sentences:
            vectors = embed_sentence([sentence.raw_content])
            vector_access.save_sentence(sentence, vectors[0])
        data_access.update_file_vectorized_count(file)


def start_parse_document(file: models.KnowledgeBaseFileTab, paragraphs: List[Paragraph]):
    vectorization_pool.submit(parse_and_vectorize_document, file, paragraphs)
