import requests
import os
import base64
import time

# sealion_notify_url = "http://notify-service"
env = os.getenv("region", "us")
if "us" in env:
    sealion_notify_url = "https://openxlab.org.cn/gw/notify-service/api/v1/notify/send_with_auth"
else:
    sealion_notify_url = "http://notify-service"


async def notify_feishu(msg: str):
    await notify(msg, "feishu", "17621502120")


async def notify(msg: str, typo: str, to: str):
    if typo == "feishu_group":
        msg = "{\"config\":{\"wide_screen_mode\":true},\"header\":{\"template\":\"orange\",\"title\":{" \
              "\"content\":\"alert\",\"tag\":\"plain_text\"}},\"i18n_elements\":{\"zh_cn\":[{\"tag\":\"div\"," \
              "\"text\":{\"content\":\"%s\",\"tag\":\"plain_text\"}}]}} " % msg
    crt_timestamp = int(time.time() * 1000)
    auth_key = f"notify::auth::alles-apin%%nipa-sella%%{crt_timestamp}"
    auth_key_base64 = base64.b64encode(auth_key.encode("utf-8")).decode("utf-8")
    header = {
        "notify_auth_key": auth_key_base64
    }
    req_body = {
        "type": typo,
        "to": to,
        "message": msg
    }
    return requests.post(url=sealion_notify_url, headers=header, json=req_body)


if __name__ == "__main__":
    notify("hello", "feishu_group", "oc_99ad443891ae5ec4d3161bfd3a31022a")
