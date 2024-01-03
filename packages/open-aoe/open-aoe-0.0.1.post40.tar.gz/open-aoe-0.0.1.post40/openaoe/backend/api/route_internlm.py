from fastapi import APIRouter, Request
from openaoe.backend.service.service_internlm import chat_completion_v1, chat_completion_stream_v1
from openaoe.backend.model.dto.OpenaiDto import OpenaiChatCompletionV2ReqDto


router = APIRouter()


@router.post("/v1/chat/completions", tags=["Internlm"])
async def internlm_chat_completions_v1(request: Request, body: OpenaiChatCompletionV2ReqDto):
    """
    Internlm ChatCompletion
    """
    # ts = get_current_ts_ms()
    ret = chat_completion_v1(request, body)
    # logger.info(f"call v1/openai/v2/text/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/chat/completions-stream", tags=["Internlm"])
async def internlm_chat_completions_v1(request: Request, body: OpenaiChatCompletionV2ReqDto):
    """
    Internlm ChatCompletion
    """
    ret = chat_completion_stream_v1(request, body)
    return ret







