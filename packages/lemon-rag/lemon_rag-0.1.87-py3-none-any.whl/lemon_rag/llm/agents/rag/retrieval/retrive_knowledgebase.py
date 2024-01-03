import re
from typing import List, Optional, Dict

from pydantic import Field

from lemon_rag.dependencies.vector_access import vector_access, DocSearchRes
from lemon_rag.lemon_runtime import models


class RelatedSentence(DocSearchRes):
    content: List[str] = Field(default_factory=list)


def retrieve_related_paragraphs(query: str, knowledgebase_id_list: List[int]):
    keys = re.split(r",.，。\n", query)
    search_res = vector_access.find_sentence(keys, knowledgebase_id_list)

    id_to_ref_mapping: Dict[int, RelatedSentence] = {}
    for hit in search_res:
        sentence: models.KnowledgeSentence = models.KnowledgeSentence.get_or_none(hit.id)
        if sentence is None:
            continue
        paragraph = sentence.paragraph
        current_ref_content = paragraph.raw_content
        if sentence.index <= paragraph.total_sentences // 3:
            former_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index - 1)
            if former_paragraph is not None:
                current_ref_content = former_paragraph.raw_content + current_ref_content
        elif sentence.index >= paragraph.total_sentences * 2 // 3:
            # 添加后一段
            next_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index + 1)
            if next_paragraph is not None:
                current_ref_content += next_paragraph.raw_content

        rp = id_to_ref_mapping.get(
            paragraph.file.id,
            RelatedSentence(doc_id=hit.doc_id, id=hit.id)
        )
        rp.content.append(current_ref_content)
        id_to_ref_mapping[paragraph.file.id] = rp

    return id_to_ref_mapping
