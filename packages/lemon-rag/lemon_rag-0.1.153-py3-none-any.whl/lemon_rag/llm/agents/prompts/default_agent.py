import datetime
import queue
from typing import List, Optional

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from playhouse.shortcuts import model_to_dict

from lemon_rag.lemon_runtime import models
from lemon_rag.llm.callback_handlers.text_callback_handler import TextCallbackHandler
from lemon_rag.llm.client.base_client import ChatChain
from lemon_rag.protocols.chat import RefFileWithContent, ResponseChunk, CompleteMessage
from lemon_rag.utils import log

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
    log.info("executing default_rag_chat, user_input=%s", user_input)
    if user_message:
        user_msg_dict = model_to_dict(user_message)
        log.info("user_msg_dict=%s", user_msg_dict)
        q.put(ResponseChunk.base_message(
            user_message.session.id,
            user_message.msg_id,
            CompleteMessage(**user_msg_dict)
        ).json())

    q.put(ResponseChunk.base_message(
        ai_message.session.id,
        ai_message.msg_id,
        CompleteMessage(**model_to_dict(ai_message))
    ).json())
    chat_chain = ChatChain(template=ChatPromptTemplate.from_strings(
        [
            (SystemMessagePromptTemplate, system_message_template),
            HumanMessage(content=user_input)
        ] + histories
    ))
    return chat_chain.run(
        callbacks=[TextCallbackHandler(q, session_id=ai_message.session.id, msg_id=ai_message.msg_id)],
        reference_paragraphs=assemble_reference_paragraphs(reference_paragraphs),
        datetime=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    )


if __name__ == '__main__':
    q = queue.Queue(maxsize=1000)
    ai_msg = models.MessageTab()
    ai_msg.msg_id = 1
    ai_msg.text = ""
    ai_msg.client_ts = 1
    ai_msg.server_ts = 1
    ai_msg.role = "ai"
    ai_msg.is_system = False
    ai_msg.is_answer = True
    ai_msg.session = models.SessionTab(
        id=1)
    default_rag_chat(
        "这个沉降缝是啥啊",
        [],
        [],
        None,
        None,
        q
    )
