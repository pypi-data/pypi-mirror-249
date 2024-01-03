from fastapi import APIRouter, Header, Request
from openaoe.backend.util.time_util import get_current_ts_ms
from openaoe.backend.util.log import log

from openaoe.backend.model.dto.BaiduDto import BaiduTransGeneralReqDto, BaiduWenxinWorkshopReqDto
from openaoe.backend.service.service_baidu import trans_general_svc

logger = log(__name__)
router = APIRouter()


@router.post("/v1/trans/general", include_in_schema=False)
async def trans_general(request: Request, body: BaiduTransGeneralReqDto, token: str = Header(alias="alles-apin-token")):
    """
    NOT Available now
    """
    ts = get_current_ts_ms()
    logger.info("start /v1/trans/general")
    ret = trans_general_svc(request, body)
    logger.info(f"end /v1/trans/general, ts= {get_current_ts_ms() - ts} ms")
    return ret
