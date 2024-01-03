#! python
import tiktoken
from openaoe.backend.util.log import log


logger = log("openai_token_calculate")


def calculate_tokens_from_messages(messages, model_name):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model_name in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model_name == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model_name:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return calculate_tokens_from_messages(messages, model_name="gpt-3.5-turbo-0613")
    elif "gpt-4" in model_name:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return calculate_tokens_from_messages(messages, model_name="gpt-4-0613")
    else:
        print(
            f"""num_tokens_from_messages() is not implemented for model {model_name}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
        return 0
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def calculate_tokens_from_text(text, model_name):
    if model_name == "gpt-3.5-turbo":
        model_name = "gpt-3.5-turbo-0613"
        return calculate_tokens_from_text(text, model_name)
    elif model_name == "gpt-4":
        model_name = "gpt-4-0613"
        return calculate_tokens_from_text(text, model_name)

    if model_name not in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        print(
            f"""num_tokens_from_messages() is not implemented for model {model_name}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
        return 0
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        res = encoding.encode(text)
    except Exception as e:
        logger.warn(f"calculate openai tokens from text failed: {e}")
        return 0
    return len(res)

