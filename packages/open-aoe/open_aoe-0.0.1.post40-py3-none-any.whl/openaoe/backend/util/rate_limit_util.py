from openaoe.backend.util.redis_ops import get, set_ex, get_ttl
from openaoe.backend.util.log import log
from openaoe.backend.config.constant import DEFAULT_RPM, USER_ID_FOR_OPENAI_CHECK, RPM_USER_QUOTA_EXCEED, RATE_LIMIT_NONE, RATE_LIMIT_QUOTA_EXCEED, RATE_LIMIT_RPM_EXCEED


logger = log(__name__)


def check_if_rate_limited(uid: str, api_type: str) -> int:
    if uid is None or uid == "":
        return True
    if api_type is None or api_type == "":
        return True
    if uid == USER_ID_FOR_OPENAI_CHECK:
        return False

    max_rpm = f"alles-apin::rate-limit::max-rpm::{uid}::{api_type}"
    crt_rpm = f"alles-apin::rate-limit::crt-rpm::{uid}::{api_type}"

    max_rpm_by_uid_path = get(max_rpm)
    # uid_path no rate limit set, set default rpm
    if max_rpm_by_uid_path is None or max_rpm_by_uid_path == "":
        max_rpm_by_uid_path = DEFAULT_RPM
    if int(max_rpm_by_uid_path) == RPM_USER_QUOTA_EXCEED:
        return RATE_LIMIT_QUOTA_EXCEED

    crt_rpm_by_uid_path = get(crt_rpm)
    # crt uid_path is empty, default to 0
    if crt_rpm_by_uid_path is None or crt_rpm_by_uid_path == "":
        crt_rpm_by_uid_path = 0

    # crt >= max, need to rate-limit
    if int(crt_rpm_by_uid_path) >= int(max_rpm_by_uid_path):
        return RATE_LIMIT_RPM_EXCEED

    # crt < max, ++crt to redis
    updated_crt_rpm_by_uid_path = int(crt_rpm_by_uid_path) + 1
    ttl = get_ttl(crt_rpm)
    if set_ex(
            key=crt_rpm,
            value=str(updated_crt_rpm_by_uid_path),
            expire_secs=ttl
    ) is False:
        logger.info(f"{crt_rpm}-{updated_crt_rpm_by_uid_path} into redis failed.")

    return RATE_LIMIT_NONE


if __name__ == '__main__':
    pass
