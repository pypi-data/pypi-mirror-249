#!/bin/python3
from openaoe.backend.config.constant import *
from openaoe.backend.util.log import log


logger = log(__name__)


class OpenAIException(Exception):
    def __init__(self, api_key, model, error, res_headers=None):
        self.api_key = api_key
        self.model = model
        self.error = error
        self.res_headers = res_headers

    def __str__(self):
        return f"[OpenAI-Exception]model: {self.model}, error: {str(self.error)}, used_key: {self.api_key}"


def is_openai_key_limited(model, e):
    if not isinstance(e, str):
        err_str = str(e)
    else:
        err_str = e

    error_reason = None

    if "Rate limit reached" in err_str:
        if "tokens per min" in err_str:
            error_reason = OPENAI_KEY_ERROR_TPM
        elif "requests per min" in err_str:
            error_reason = OPENAI_KEY_ERROR_RPM
        elif "tokens per day" in err_str:
            error_reason = OPENAI_KEY_ERROR_TPD
        elif "requests per day" in err_str:
            error_reason = OPENAI_KEY_ERROR_RPD
        else:
            print(f"model: {model} has error string: {err_str}, reason unknown")
    elif "You exceeded your current quota" in err_str:
        error_reason = OPENAI_KEY_ERROR_QUOTA
    elif "not active" in err_str:
        error_reason = OPENAI_KEY_ERROR_INVALID

    if error_reason:
        return True, error_reason
    return False, None

