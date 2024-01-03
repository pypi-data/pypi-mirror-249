import re
from collections import defaultdict
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

    all_paragraphs: List[models.KnowledgeParagraph] = []
    for res in search_res:
        sentence: models.KnowledgeSentence = models.KnowledgeSentence.get_or_none(res.id)
        if sentence is None:
            continue
        paragraph = sentence.paragraph
        log.info(
            "use paragraph id=%s, hit=%s, index=%s/%s",
            paragraph.id, res, sentence.index, paragraph.total_sentences // 3
        )
        hit_paragraphs = [paragraph]
        current_ref_content = paragraph.raw_content
        if sentence.index <= paragraph.total_sentences // 3:
            former_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index - 1)
            if former_paragraph is not None:
                hit_paragraphs = [former_paragraph] + hit_paragraphs
        elif sentence.index >= paragraph.total_sentences * 2 // 3:
            # 添加后一段
            next_paragraph: Optional[models.KnowledgeParagraph] = models.KnowledgeParagraph.get_or_none(
                file=paragraph.file, index=paragraph.index + 1)
            if next_paragraph is not None:
                hit_paragraphs.append(next_paragraph)
                log.info("add next paragraph id=%s", next_paragraph.id)

        all_paragraphs.extend(hit_paragraphs)
    distinct_paragraphs = sorted(set(all_paragraphs), key=lambda p: (p.file.id, p.index))
    result = Dict[int, List[str]] = defaultdict(list)
    for p in distinct_paragraphs:
        result[p.file.id].append(p.raw_content)
    return result
