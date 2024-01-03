import jwt
import datetime
from typing import Optional
from openaoe.backend.config.biz_config import jwt_cfg
from openaoe.backend.util.redis_ops import get
from openaoe.backend.util.log import log
from openaoe.backend.config.constant import TOKEN_FOR_OPENAI_CHECK, USER_ID_FOR_OPENAI_CHECK

logger = log(__name__)

# 配置
SECRET_KEY = jwt_cfg.get("jwt_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_WEEKS = 600


def encode_jwt(payload: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = payload.copy()
    if expires_delta is not None:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.JWTError as e:
        print(f"Error: {e}")
        return {}


def check_jwt_if_valid(token: str) -> str:
    if token is None or token == "":
        return ""

    if token == TOKEN_FOR_OPENAI_CHECK:
        return USER_ID_FOR_OPENAI_CHECK

    jwt_dict = decode_jwt(token)
    if jwt_dict is {}:
        return ""
    user_id = jwt_dict.get("user_id")
    s = get(f"alles-apin::auth::jwt::uid::{user_id}")
    if s is None or s == "":
        logger.info(f"get token by {user_id} from redis is empty")
        return ""
    if token != s:
        logger.info("request token not equals to the token in redis")
        return ""
    return user_id
