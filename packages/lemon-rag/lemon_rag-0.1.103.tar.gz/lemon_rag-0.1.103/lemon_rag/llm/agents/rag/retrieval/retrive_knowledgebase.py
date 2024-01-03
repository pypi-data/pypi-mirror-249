import re
from typing import List, Optional, Dict

from pydantic import Field

from lemon_rag.dependencies.vector_access import vector_access, DocSearchRes
from lemon_rag.lemon_runtime import models
from lemon_rag.utils import log


class RelatedSentence(DocSearchRes):
    content: List[str] = Field(default_factory=list)


def retrieve_related_paragraphs(query: str, knowledgebase_id_list: List[int]):
    keys = re.split(r",.，。\n", query)
    search_res = vector_access.find_sentences(keys, knowledgebase_id_list)

    id_to_ref_mapping: Dict[int, RelatedSentence] = {}
    for res in search_res:
        sentence: models.KnowledgeSentence = models.KnowledgeSentence.get_or_none(res.id)
        if sentence is None:
            continue
        paragraph = sentence.paragraph
        log.info(
            "use paragraph id=%s, hit=%s, index=%s/%s",
            paragraph.id, res, sentence.index, paragraph.total_sentences // 3
        )
        current_ref_content = paragraph.raw_content
        if sentence.index <= paragraph.total_sentences // 3:
            former_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index - 1)
            if former_paragraph is not None:
                current_ref_content = former_paragraph.raw_content + current_ref_content
                log.info("add former paragraph id=%s", former_paragraph.id)

        elif sentence.index >= paragraph.total_sentences * 2 // 3:
            # 添加后一段
            next_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index + 1)
            if next_paragraph is not None:
                current_ref_content += next_paragraph.raw_content
                log.info("add next paragraph id=%s", next_paragraph.id)

        rp = id_to_ref_mapping.get(
            paragraph.file.id,
            RelatedSentence(doc_id=res.doc_id, id=res.id)
        )
        rp.content.append(current_ref_content)
        id_to_ref_mapping[paragraph.file.id] = rp

    return id_to_ref_mapping
