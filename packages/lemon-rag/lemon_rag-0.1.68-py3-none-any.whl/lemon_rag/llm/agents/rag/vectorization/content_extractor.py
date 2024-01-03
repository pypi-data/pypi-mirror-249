import abc
import io
import re
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class FileExtension(str, Enum):
    doc = "doc"
    docx = "docx"
    pdf = "pdf"
    txt = "txt"

    @classmethod
    def _missing_(cls, value: str) -> 'FileExtension':
        value = value.lower()
        return FileExtension(value)


class Paragraph(BaseModel):
    index: int = 0
    sentences: List[str] = []


class ContentExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_content(self, file_path: Union[str, io.IOBase]) -> List[Paragraph]:
        pass


def split_text(document: str) -> List[str]:
    delimiter_pattern = r'([\n。！？.!?])'
    segments = re.split(delimiter_pattern, document)
    sentences = [segments[i] + segments[i + 1] for i in range(0, len(segments) - 1, 2)]
    return sentences


class TxtExtractor(ContentExtractor):
    paragraph_threshold = 300  # paragraph 必须是有换行分割、符号分割
    sentence_threshold = 30

    def extract_content(self, file_path: Union[str, io.IOBase]) -> List[Paragraph]:
        if isinstance(file_path, io.IOBase):
            content = file_path.read()
        else:
            with open(file_path, "r") as f:
                content = f.read()
        res: List[Paragraph] = []
        current_paragraph: Optional[Paragraph] = None

        for sentence in split_text(content):
            if not current_paragraph or len("".join(current_paragraph.sentences)) >= self.paragraph_threshold:
                current_paragraph = Paragraph()
                res.append(current_paragraph)
            current_paragraph.sentences.append(sentence)
        return res
