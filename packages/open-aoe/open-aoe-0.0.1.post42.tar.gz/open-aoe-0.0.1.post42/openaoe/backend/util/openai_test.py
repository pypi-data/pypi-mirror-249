import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import openai
import requests
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = '47.88.91.12:9999/openai/v1'
headers = {
    "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImxpdWt1aWt1biIsImFwcGx5X2F0IjoxNjg1NTE4OTY0MjA4LCJleHAiOjE4NjY5NTg5NjR9.Rb1jHeoPiYqplsn1Qk1rgPbOiNeovtCFwHa92YPR3Xo",
    "content-type": "application/json"
}


def send_request_2(prompt):
    time.sleep(0.1)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 400
    }
    response = requests.post(
        url="http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/openai/v2/text/chat",
        # url="http://127.0.0.1:10029/v1/openai/v2/text/chat",
        headers=headers,
        json=data
    )
    msg_code = response.json().get("msgCode")
    if msg_code != "10000":
        print(response.json().get("data"))
        return "", None
    response = response.json().get("data")
    answer = response["choices"][0]["message"]["content"]
    tokens = response["usage"]["total_tokens"]
    return answer, tokens


def send_request_1(prompt):
    time.sleep(0.1)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 200
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        request_timeout=10,
    )
    answer = response["choices"][0]["message"]["content"]
    tokens = response["usage"]["total_tokens"]
    return answer, tokens


prompts = ["Please tell a love story with at lease 300 words" for _ in range(1000)]
results = []
workers = 50
tokens = 0



start = time.time()
with ThreadPoolExecutor(max_workers=workers) as executor:
    tasks = (executor.submit(send_request_2, prompt) for prompt in prompts)
    for future in tqdm(as_completed(tasks), total=len(prompts)):
        try:
            data = future.result()
            print(data[0])
        except Exception as ex:
            print(f"ex={ex}")
        else:
            results.append(data[0])
            tokens += data[1]
end = time.time()

print(f"{int(len(results) * 60 / (end - start))} RPM")
print(f"{int(tokens * 60 / (end - start))} TPM")
