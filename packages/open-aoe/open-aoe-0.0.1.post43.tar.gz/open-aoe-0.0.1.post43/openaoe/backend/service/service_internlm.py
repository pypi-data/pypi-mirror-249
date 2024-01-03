from openaoe.backend.model.dto.OpenaiDto import OpenaiChatCompletionV2ReqDto
from sse_starlette.sse import EventSourceResponse
from openaoe.backend.model.dto.ReturnBase import ReturnBase
import json
from openaoe.backend.util.exception import *
from fastapi.encoders import jsonable_encoder
from openaoe.backend.config.biz_config import get_base_url
import requests


logger = log(__name__)


def get_req_params_v2(req_dto: OpenaiChatCompletionV2ReqDto):
    model = req_dto.model
    messages = req_dto.messages
    temperature = req_dto.temperature
    max_tokens = req_dto.max_tokens
    top_p = req_dto.top_p
    n = req_dto.n
    presence_penalty = req_dto.presence_penalty
    frequency_penalty = req_dto.frequency_penalty
    api_base = get_base_url(VENDOR_INTERNLM)
    stream = req_dto.stream
    return model, messages, temperature, max_tokens, top_p, n, presence_penalty, frequency_penalty, api_base, stream


def chat_completion_v1(request, req_dto: OpenaiChatCompletionV2ReqDto):
    model, messages, temperature, max_tokens, top_p, n, presence_penalty, frequency_penalty, api_base, stream = get_req_params_v2(
        req_dto)
    msgs = []
    for msg in messages:
        msg_item = {
            "role": msg.role,
            "content": jsonable_encoder(msg.content),
        }
        msgs.append(msg_item)

    # restful api
    url = api_base+"/v1/chat/completions"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "model": model,
        "messages": msgs,
        "temperature": temperature,
        "top_p": top_p,
        "n": n,
        "max_tokens": max_tokens,
        "stop": False,
        "stream": stream,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "user": "string",
        "repetition_penalty": 1,
        "session_id": -1,
        "ignore_eos": False
    }
    if not stream:
        res = requests.post(url, headers=headers, json=data)
        if res and res.status_code == 200:
            base = ReturnBase(
                data=res.json()
            )
            return base
        else:
            return ReturnBase(
                data="request failed"
            )
    else:
        return chat_completion_stream_v1(request, url, headers, data)


def chat_completion_stream_v1(request, url, headers, data):
    async def event_generator_json():
        while True:
            stop_flag = False
            response = ""
            if await request.is_disconnected():
                break
            try:
                res = requests.post(url, headers=headers, json=data)
                res_data = res.text.replace("data: ", "")
                json_strings = res_data.split("\n\n")
                # 解析 JSON 数据
                for chunk in json_strings:
                    try:
                        json_data = json.loads(chunk)
                        choice = json_data["choices"][0]
                        if choice['finish_reason']:
                            stop_flag = True
                        if 'content' not in choice['delta']:
                            continue
                        s = choice["delta"]["content"]
                        if s:
                            response += s
                            dict_item = {
                                "success": "true",
                                "msg": s
                            }
                            yield json.dumps(dict_item, ensure_ascii=False)
                        if stop_flag:
                            break
                    except json.JSONDecodeError as e:
                        print(f"JSON Parse Error: {e}")

                if stop_flag:
                    break
            except Exception as e:
                yield json.dumps({
                    "success": "false",
                    "msg": str(e)
                })
                break

    return EventSourceResponse(event_generator_json())



if __name__ == "__main__":
    pass



# curl 127.0.0.1:10029/v1/openai/v1/text/chat-stream -X POST -d '{"model":"gpt-3.5-turbo-0301","prompt":"给我写一首200个字的诗， 用英文", "stream": true}' -H 'content-type: application/json'
# curl https://beta.openxlab.org.cn/gw/alles-apin/v1/openai/v1/text/chat-stream -X POST -d '{"model":"gpt-3.5-turbo-0301","prompt":"给我写一首200个字的诗， 用英文", "stream": true}' -H 'content-type: application/json'
