import redis
import os
from typing import Union


env = os.environ.get("region")
redis_cfg = {
    "dev": {
        "host": "openmmlab-dev-out.redis.rds.aliyuncs.com",
        "port": 6379,
        "password": "MbOqoTxGiYerU6B2",
        "db": 0
    },
    "staging": {
        "host": "openmmlab-dev-out.redis.rds.aliyuncs.com",
        "port": 6379,
        "password": "MbOqoTxGiYerU6B2",
        "db": 0
    },
    "prod": {
        "host": "openmmlab-dev-out.redis.rds.aliyuncs.com",
        "port": 6379,
        "password": "MbOqoTxGiYerU6B2",
        "db": 0
    },
    "us": {
        "host": "openmmlab-us-sv-out.redis.rds.aliyuncs.com",
        "port": 6379,
        "password": "qVDG5i730XwUncgl",
        "db": 0
    },
}


if env is None:
    env = "dev"
    print(f"environment is empty, use default value: {env}")


r = redis.Redis(
    host=redis_cfg.get(env).get("host"),
    port=redis_cfg.get(env).get("port"),
    db=redis_cfg.get(env).get("db"),
    password=redis_cfg.get(env).get("password")
)


def get(key: str) -> str:
    value = r.get(key)
    if value is not None:
        return value.decode('utf-8')
    else:
        return ''


def set_ex(key: str, value: str, expire_secs: int) -> bool:
    if key is None or value is None:
        return False
    if expire_secs is None or expire_secs <= 0:
        return False
    return r.setex(key, expire_secs, value.encode('utf-8'))


def set_nx(key: str, value: str) -> bool:
    if key is None or value is None:
        return False
    return r.setnx(key, value.encode('utf-8'))


def set_always(key: str, value: str) -> bool:
    if key is None or value is None:
        return False
    return r.set(key, value.encode('utf-8'))


def update(key: str, value: str) -> bool:
    if key is None or value is None:
        return False
    return r.set(key, value)


def get_ttl(key: str) -> Union[int, None]:
    if key is None:
        return None
    exist_ttl = r.ttl(key)
    if exist_ttl > 0:
        return exist_ttl
    return 60


def getAllReqCounts():
    redis_prefix_key = "alles-apin::req-record"
    all_apis = [
        "/v1/baidu/v1/trans/general",
        "/v1/baidu/v1/wenxinworkshop/chat",
        "/v1/claude/v1/text/chat_by_slack",
        "/v1/google/v1/palm/chat",
        "/v1/google/v1/palm/text",
        "/v1/minimax/v1/text/chat",
        "/v1/minimax/v1/text/chat-stream"
        "/v1/openai/v1/text/chat",
        "/v1/openai/v2/text/chat",
        "/v1/openai/v1/text/chat-stream",
        "/v1/openai/v1/completions"
    ]
    for i in range(12):
        for api in all_apis:
            key = f"{redis_prefix_key}::{i}::{api}"
            value = get(key)
            if value is not None and value != "":
                print(f"{key}:{value}")


def zincrby(key: str, offset: float, member: str):
    if key is None or member is None:
        return False
    return r.zincrby(key, offset, member)


if __name__ == "__main__":
    getAllReqCounts()
    pass
