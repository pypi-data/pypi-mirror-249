# api examples

def openai_chat_completion_v1_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "请作为AI助手回答问题"
                },
                {
                    "role": "assistant",
                    "content": "好的"
                },
                {
                    "role": "user",
                    "content": "请讲一个无伤大雅的笑话"
                }
            ]
        }
        },
        "chat-with-function-call": {
            "summary": "chat-with-function-call",
            "description": "for now, only support model: gpt-4-0613, gpt-3.5-turbo-0613 (check https://openai.com/blog/function-calling-and-other-api-updates)",
            "value": {
                "model": "gpt-3.5-turbo-0613",
                "prompt": "what's the weather in shanghai, represent with celsius",
                "functions": [
                    {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA"
                                },
                                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                            },
                            "required": ["location"]
                        }
                    }
                ],
                "messages": [{
                    "role": "system",
                    "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
                }],
                "role_meta": {
                    "user_name": "user",
                    "bot_name": "assistant"
                }
            }
        }
    }


def openai_chat_completion_v2_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                      "role": "user",
                      "content": "请作为AI助手回答问题"
                    },
                    {
                        "role": "assistant",
                        "content": "好的"
                    },
                    {
                        "role": "user",
                        "content": "请讲一个无伤大雅的笑话"
                    }
                ]
            }
        },
        "chat-with-function-call": {
            "summary": "chat-with-function-call",
            "description": "for now, only support model: gpt-4-0613, gpt-3.5-turbo-0613 (check https://openai.com/blog/function-calling-and-other-api-updates)",
            "value": {
                "model": "gpt-3.5-turbo-0613",
                "messages": [
                    {
                      "role": "user",
                      "content": "请作为AI助手回答问题"
                    },
                    {
                        "role": "assistant",
                        "content": "好的"
                    },
                    {
                        "role": "user",
                        "content": "上海的天气是？"
                    }
                ],
                "functions": [
                    {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA"
                                },
                                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                            },
                            "required": ["location"]
                        }
                    }
                ]
            }
        }
    }


def openai_chat_stream_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "gpt-3.5-turbo",
                "prompt": "请讲一个无伤大雅的笑话",
                "role_meta": {
                    "user_name": "user",
                    "bot_name": "ai"
                },
                "messages": [
                    {
                      "sender_type": "user",
                      "text": "请作为AI助手回答问题"
                    },
                    {
                        "sender_type": "ai",
                        "text": "好的"
                    }
                ],
                "type": "json"
            }
        },
        # pending forever
        # "chat-with-function-call": {
        #     "summary": "chat-with-function-call",
        #     "description": "for now, only support model: gpt-4-0613, gpt-3.5-turbo-0613 (check https://openai.com/blog/function-calling-and-other-api-updates)",
        #     "value": {
        #         "model": "gpt-3.5-turbo-0613",
        #         "prompt": "上海的天气是？",
        #         "role_meta": {
        #             "user_name": "user",
        #             "bot_name": "ai"
        #         },
        #         "messages": [
        #             {
        #               "sender_type": "user",
        #               "text": "请作为AI助手回答问题"
        #             },
        #             {
        #                 "sender_type": "ai",
        #                 "text": "好的"
        #             }
        #         ],
        #         "type": "json",
        #         "functions": [
        #             {
        #                 "name": "get_current_weather",
        #                 "description": "Get the current weather in a given location",
        #                 "parameters": {
        #                     "type": "object",
        #                     "properties": {
        #                         "location": {
        #                             "type": "string",
        #                             "description": "The city and state, e.g. San Francisco, CA"
        #                         },
        #                         "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        #                     },
        #                     "required": ["location"]
        #                 }
        #             }
        #         ]
        #     }
        # }
    }


def minimax_chat_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "abab5-chat",
                "prompt": "请作为AI助手，和我谈话",
                "role_meta": {
                    "user_name": "user",
                    "bot_name": "ai"
                },
                "messages": [
                    {
                      "sender_type": "USER",
                      "text": "你好"
                    },
                    {
                        "sender_type": "BOT",
                        "text": "你好！我很高兴为你服务。你需要了解什么？"
                    },
                    {
                        "sender_type": "USER",
                        "text": "请讲一个无伤大雅的笑话"
                    }
                ],
                "type": "text"
            }
        }
    }


def spark_chat_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "parameter": {
                    "chat": {
                        "temperature": 0.5,
                        "max_tokens": 1024,
                        "chat_id": "user1"
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {"role": "user", "content": "请编写一道鸡兔同笼问题（不需要解答）"},
                            {"role": "assistant", "content": "好的，这是一道经典的鸡兔同笼问题： \n在一个大笼子里，有一些鸡和兔子。你数了数，一共有30个头，94只脚。请问，这个笼子里有多少只鸡，多少只兔子？"},
                            {"role": "user", "content": "请详细解答上面的问题"}
                        ]
                    }
                }
            }
        }
    }


def palm_chat_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "chat-bison-001",
                "prompt": {
                    "messages": [{
                        "content": "hello",
                        "author": "user"
                    }]
                }
            }
        }
    }


def palm_text_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "text-bison-001",
                "prompt": {
                    "text": "tell me a joke"
                }
            }
        }
    }


def claude_examples():
    return {
        "chat": {
            "summary": "chat",
            "value": {
                "model": "claude-instant-1",
                "prompt": "请讲一个无伤大雅的笑话",
                "messages": [{
                        "role": "user",
                        "content": "hello"
                    },{
                        "role": "bot",
                        "content": "Hello! My name is Claude. Nice to meet you!"
                    }, {
                        "role": "user",
                        "content": "请预测未来世界形势"
                    }]
            }
        }
    }