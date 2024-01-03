import requests
from openaoe.backend.config.constant import *
from openaoe.backend.model.dto.BaiduDto import BaiduTransGeneralReqDto
from openaoe.backend.util.encrypt_util import md5_generate
from openaoe.backend.util.log import log
from openaoe.backend.util.time_util import get_current_ts_ms
from openaoe.backend.model.dto.ReturnBase import ReturnBase
from openaoe.backend.config.biz_config import get_configuration

logger = log(__name__)


def trans_general_svc(request, req_dto: BaiduTransGeneralReqDto):
    base_url = get_configuration(VENDOR_BAIDU, "translation_api_base")
    ak = get_configuration(VENDOR_BAIDU, "ak")
    sk = get_configuration(VENDOR_BAIDU, "sk")
    q = req_dto.q
    frm = req_dto.frm
    to = req_dto.to
    salt = get_current_ts_ms()
    sign = md5_generate(f"{ak}{q}{salt}{sk}")
    url = f"{base_url}?q={q}&from={frm}&to={to}&appid={ak}&salt={salt}&sign={sign}"
    logger.info(f"calling baidu api url: {url}")
    response = requests.get(url)
    response_json = response.json()
    err_code = response_json.get("error_code")

    if err_code is not None:
        err_msg = response_json.get("error_msg")
        base = ReturnBase(
            msgCode="-1",
            msg=f"call baidu api failed, appid={ak}. Detail reason: {err_msg}"
        )
        return base
    base = ReturnBase(
        data=response_json
    )
    return base


if __name__ == "__main__":
    pass
