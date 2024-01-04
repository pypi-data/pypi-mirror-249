import datetime
import queue
from typing import List, Tuple, Type, Optional

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from playhouse.shortcuts import model_to_dict

from lemon_rag.lemon_runtime import models
from lemon_rag.llm.callback_handlers.text_callback_handler import TextCallbackHandler
from lemon_rag.llm.client.base_client import create_openai_fn_chain, ChatChain
from lemon_rag.protocols.chat import RefFileWithContent, ChatRole, ResponseChunk, CompleteMessage

system_message_template = """
# Role
You are a awesome assistant. Your responsibility is to assist the user in managing their renovation projects and keeping track of expenses.
* If the user want to record something, you need to call the property function to do that.
* If the user want to query some complicated data, you need to call the function to do that.
* If the user want to ask something about the standard, you need to ask the question based on the given references. When you answer a question, the markdown format is preferred.

You are available to use some tools which is offered as function calls. You can call the function to satisfy the user's requirement if necessary.

Here are some reference data:
{reference_paragraphs}


Now it is {datetime}, Now please start to assistant the user.
"""


def assemble_reference_paragraphs(reference_paragraphs: List[RefFileWithContent]) -> str:
    lines = []
    for ref in reference_paragraphs:
        lines.append(f"# {ref.origin_filename}")
        for c in ref.content:
            lines.append(c)
    return "\n".join(lines)


def default_rag_chat(
        user_input: str,
        histories: List[BaseMessage],
        reference_paragraphs: List[RefFileWithContent],
        user_message: Optional[models.MessageTab],
        ai_message: models.MessageTab,
        q: queue.Queue
) -> str:
    if user_message:
        q.put(ResponseChunk.base_message(
            user_message.session.id,
            user_message.msg_id,
            CompleteMessage(**model_to_dict(user_message))
        ))
    q.put(ResponseChunk.base_message(
        ai_message.session.id,
        ai_message.msg_id,
        CompleteMessage(**model_to_dict(ai_message))
    ))
    chat_chain = ChatChain(template=ChatPromptTemplate.from_strings(
        [
            (SystemMessagePromptTemplate, system_message_template),
            HumanMessage(content=user_input)
        ] + histories
    ))
    return chat_chain.run(
        callbacks=[TextCallbackHandler(q)],
        reference_paragraphs=assemble_reference_paragraphs(reference_paragraphs),
        datetime=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    )
