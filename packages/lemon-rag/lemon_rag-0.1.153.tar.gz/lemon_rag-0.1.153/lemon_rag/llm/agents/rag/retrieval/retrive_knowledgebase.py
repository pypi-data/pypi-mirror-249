import re
from typing import List, Optional, Dict

from pydantic import BaseModel

from lemon_rag.dependencies.vector_access import vector_access
from lemon_rag.lemon_runtime import models
from lemon_rag.protocols.chat import RefFileWithContent
from lemon_rag.utils import log


class RelatedParagraphRes(BaseModel):
    file_to_content_mapping: Dict[int, List[str]]
    paragraphs: List[int]


def retrieve_related_paragraphs(query: str, file_id_list: List[int]) -> Dict[int, RelatedParagraphRes]:
    keys = re.split(r",.，。\n", query)
    search_res = vector_access.find_sentences(keys, file_id_list)

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
    result: Dict[int, RefFileWithContent] = {}
    for index, p in enumerate(distinct_paragraphs):
        if result.get(p.file.id) is None:
            result[p.file.id] = RefFileWithContent(
                id=p.file.id,
                origin_filename=p.file.origin_filename,
                extension=p.file.extension,
                file_size=p.file.file_size
            )
        if index > 0 and (
                last_p := distinct_paragraphs[
                    index - 1]) and last_p.file.id == p.file.id and last_p.index == p.index - 1:
            result[p.file.id].content[-1] += p.raw_content

        else:
            result[p.file.id].content.append(p.raw_content)
        result[p.file.id].paragraph_id_list.append(p.id)
    return result
