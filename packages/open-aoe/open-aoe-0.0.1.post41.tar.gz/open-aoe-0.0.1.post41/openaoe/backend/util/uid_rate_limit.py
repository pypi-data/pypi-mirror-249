# 设置账号限流
# apis 是所有需要被限流的接口列表
# uids 是所有需要被限流的用户ids
# 国内部署的alles-apin: environment=dev &&python uid_rate_limit.py
# 美国部署的alles-apin: environment=us &&python uid_rate_limit.py

from redis_ops import set_nx

apis = [
    # "/v1/baidu/v1/trans/general",
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


redis_prefix_key = 'alles-apin::rate-limit::max-rpm'
uids = [
    "5"
]


for uid in uids:
    for api in apis:
        redis_key = f"{redis_prefix_key}::{uid}::{api}"
        print(f"setting redis_key={redis_key}")
        if not set_nx(redis_key, "0"):
            print(f"set redis key={redis_key} failed")


