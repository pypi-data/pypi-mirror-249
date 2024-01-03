from openaoe.backend.util.redis_ops import env
from openaoe.backend.config import constant


def is_us():
    return env == constant.ENV_US
