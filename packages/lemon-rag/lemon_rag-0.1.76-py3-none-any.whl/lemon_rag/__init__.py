from lemon_rag.api.auth import hello_world, hello_stream, register
from lemon_rag.api.base import handle_all_api
from lemon_rag.patch.patch_vars import patch_all
import lemon_rag.api.chat

debug_exec = exec
