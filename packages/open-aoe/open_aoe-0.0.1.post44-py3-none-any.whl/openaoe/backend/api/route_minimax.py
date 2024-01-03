from fastapi import APIRouter, Request, Header, Body
from openaoe.backend.service.service_minimax import chat_completion, minimax_chat_stream_svc
from openaoe.backend.model.dto.MinimaxDto import MinimaxChatCompletionReqDto
from openaoe.backend.util.log import log
from openaoe.backend.util.example import *

logger = log(__name__)
router = APIRouter()


@router.post("/v1/text/chat", tags=["MiniMax"])
async def minimax_chat(request: Request, body: MinimaxChatCompletionReqDto = Body(openapi_examples=minimax_chat_examples()), token: str = Header(alias="alles-apin-token")):
    """
    prompt 表示对话前提 \n
    []messages 表示历史对话记录，其中sender_type固定取值为USER/BOT
    """
    # ts = get_current_ts_ms()
    # logger.info("start /v1/minimax/v1/text/chat")
    ret = chat_completion(request, body)
    # logger.info(f"end /v1/minimax/v1/text/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/text/chat-stream", tags=["MiniMax"])
async def minimax_chat_stream(request: Request, req_dto: MinimaxChatCompletionReqDto = Body(openapi_examples=minimax_chat_examples()), token: str = Header(alias="alles-apin-token")):
    """
    prompt 表示对话前提\n
    []messages 表示历史对话记录，其中sender_type固定取值为USER/BOT
    """
    # ts = get_current_ts_ms()
    # logger.info("start /v1/minimax/v1/text/chat-stream")
    req_dto.stream = True
    ret = minimax_chat_stream_svc(request, req_dto)
    # logger.info(f"end /v1/minimax/v1/text/chat-stream, ts= {get_current_ts_ms() - ts} ms")
    return ret
