from fastapi import APIRouter, Header, Body, Request
from openaoe.backend.service.service_google import palm_chat_svc, palm_text_svc, bard_ask_img_svc
from openaoe.backend.model.dto.GoogleDto import GooglePalmChatReqDto, GooglePalmTextReqDto, GoogleBardAskImgReqDto
from openaoe.backend.util.log import log
from openaoe.backend.util.example import *

logger = log(__name__)
router = APIRouter()


@router.post("/v1/palm/chat", tags=["PaLM"])
async def palm_chat(request: Request, body: GooglePalmChatReqDto = Body(openapi_examples=palm_chat_examples()), token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    # logger.info("start /v1/palm/chat")
    ret = palm_chat_svc(request, body)
    # logger.info(f"end /v1/palm/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/palm/text", tags=["PaLM"])
async def palm_chat(request: Request, body: GooglePalmTextReqDto = Body(openapi_examples=palm_text_examples()), token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    # logger.info("start /v1/palm/text")
    ret = palm_text_svc(request, body)
    # logger.info(f"end /v1/palm/text, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/bard/ask_about_image", tags=["PaLM"], include_in_schema=False)
async def palm_chat(body: GoogleBardAskImgReqDto, token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    # logger.info("start /v1/bard/ask_about_image")
    ret = bard_ask_img_svc(body)
    # logger.info(f"end /v1/bard/ask_about_image, ts= {get_current_ts_ms() - ts} ms")
    return ret
