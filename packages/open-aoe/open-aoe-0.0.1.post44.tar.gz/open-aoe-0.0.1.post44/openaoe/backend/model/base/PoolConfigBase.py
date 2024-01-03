#!/usr/bin/python3
import json
import sys


class PoolConfig:

    def __init__(self, keys, users, blacklist):
        self._keys = keys
        self._users = users
        self._blacklist = blacklist

    @classmethod
    def convert(cls, s: str):
        j = json.loads(s)

        return PoolConfig(j["keys"], j["users"], j["blacklist"])

    def get_user_vendor_key_name(self, user_id: str, vendor_name: str) -> str:
        if vendor_name not in self._users:
            print(f"invalid {vendor_name} to get key name")
            sys.exit(1)

        m = self._users[vendor_name]
        if user_id not in m:
            return m["default"]
        return m[user_id]

    def set_keys(self, share_memory: dict, lock):
        lock.acquire()
        for k, v in self._keys.items():
            share_memory[k] = v
        lock.release()

    def get_keys(self, key_name, share_memory: dict, lock):
        with lock:
            if key_name not in share_memory:
                return []
            return share_memory[key_name]

    def get_blacklist(self, lock):
        with lock:
            return self._blacklist

    def update_blacklist(self, lock, blacklist):
        with lock:
            self._blacklist = blacklist

    # 新增 指定模型对应key 到黑名单（并标明截止时间）
    def add_blacklist_item(self, lock, model_name, key, end_timestamp):
        with lock:
            if not self._blacklist.get(model_name):
                self._blacklist[model_name] = {}
            self._blacklist[model_name][key] = end_timestamp


if __name__ == "__main__":
    a = """{
    "users": {
        "openai-gpt35": {
            "1": "gpt35-pool-a",
            "default": "gpt35-default"
        }
    },
    "keys": {
        "gpt35-pool-a": [],
        "gpt35-default": []
    }
}"""
    p = PoolConfig.convert(a)
    print(p.get_user_vendor_key_name("1", "openai-gpt35"))

