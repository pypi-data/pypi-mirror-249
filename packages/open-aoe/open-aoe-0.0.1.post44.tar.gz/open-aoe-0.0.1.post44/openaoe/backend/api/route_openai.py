from fastapi import APIRouter, Request, Body
from fastapi import Header
from openaoe.backend.service.service_openai import chat_completion, completions, chat_completion_stream, chat_completion_v2, \
    proxy_files, proxy_assistants, proxy_threads, proxy_messages, proxy_runs
from openaoe.backend.model.dto.OpenaiDto import OpenaiChatCompletionReqDto, OpenaiCompletionReqDto, OpenaiChatStreamReqDto, \
    OpenaiChatCompletionV2ReqDto, OpenaiCheckReqDto
from openaoe.backend.util.log import log
from openaoe.backend.util.example import *

logger = log(__name__)
router = APIRouter()


@router.post("/v1/text/chat", tags=["OpenAI"])
async def openai_chat(request: Request,
                      body: OpenaiChatCompletionReqDto = Body(openapi_examples=openai_chat_completion_v1_examples()),
                      ):
    """
    OpenAI ChatCompletion
    """
    # ts = get_current_ts_ms()
    ret = chat_completion(request, body)
    # logger.info(f"call v1/openai/v1/text/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v2/text/chat", tags=["OpenAI"])
async def openai_chat_v2(request: Request, body: OpenaiChatCompletionV2ReqDto = Body(
    openapi_examples=openai_chat_completion_v2_examples())):
    """
    OpenAI ChatCompletion
    """
    # ts = get_current_ts_ms()
    ret = chat_completion_v2(request, body)
    # logger.info(f"call v1/openai/v2/text/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/completions", include_in_schema=False, tags=["OpenAI"])
async def openai_completions(request: Request, body: OpenaiCompletionReqDto):
    """
    OpenAI completion
    """
    # ts = get_current_ts_ms()
    ret = completions(request, body)
    # logger.info(f"call v1/openai/v1/completions, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/text/chat-stream", tags=["OpenAI"])
async def openai_chat_stream(request: Request,
                             req_dto: OpenaiChatStreamReqDto = Body(openapi_examples=openai_chat_stream_examples())):
    """
    OpenAI ChatCompletion with Stream
    """
    # ts = get_current_ts_ms()
    ret = chat_completion_stream(request, req_dto)
    # logger.info(f"call v1/openai/v1/text/chat-stream, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.get("/v1/files", include_in_schema=False)
@router.post("/v1/files", include_in_schema=False)
@router.get("/v1/files/{id}", include_in_schema=False)
@router.get("/v1/files/{id}/content", include_in_schema=False)
@router.delete("/v1/files/{id}", include_in_schema=False)
async def proxy_for_files(request: Request):
    ret = await proxy_files(request)
    return ret


@router.get("/v1/assistants", include_in_schema=False)
@router.post("/v1/assistants", include_in_schema=False)
@router.get("/v1/assistants/{id}", include_in_schema=False)
@router.post("/v1/assistants/{id}", include_in_schema=False)
@router.delete("/v1/assistants/{id}", include_in_schema=False)
async def proxy_for_assistants(request: Request):
    ret = await proxy_assistants(request)
    return ret


@router.post("/v1/threads", include_in_schema=False)
@router.get("/v1/threads/{id}", include_in_schema=False)
@router.post("/v1/threads/{id}", include_in_schema=False)
@router.delete("/v1/threads/{id}", include_in_schema=False)
async def proxy_for_threads(request: Request):
    ret = await proxy_threads(request)
    return ret


@router.get("/v1/threads/{id}/messages", include_in_schema=False)
@router.post("/v1/threads/{id}/messages", include_in_schema=False)
@router.get("/v1/threads/{id}/messages/{message_id}", include_in_schema=False)
@router.post("/v1/threads/{id}/messages/{message_id}", include_in_schema=False)
async def proxy_for_messages(request: Request):
    ret = await proxy_messages(request)
    return ret


@router.get("/v1/threads/{id}/runs", include_in_schema=False)
@router.post("/v1/threads/{id}/runs", include_in_schema=False)
@router.get("/v1/threads/{id}/runs/{run_id}", include_in_schema=False)
@router.post("/v1/threads/{id}/runs/{run_id}", include_in_schema=False)
@router.post("/v1/threads/{id}/runs/{run_id}/submit_tool_outputs", include_in_schema=False)
@router.post("/v1/threads/{id}/runs/{run_id}/cancel", include_in_schema=False)
@router.get("/v1/threads/{id}/runs/{run_id}/steps/{step_id}", include_in_schema=False)
@router.get("/v1/threads/{id}/runs/{run_id}/steps", include_in_schema=False)
async def proxy_for_runs(request: Request):
    ret = await proxy_runs(request)
    return ret
