from pydantic import BaseModel
from typing import Optional


class ClaudeSlackChatReqDto(BaseModel):
    """
        see
        - claude_wrapper.py (使用@张松阳 的 claude 账户，暂时无法保证 context free，只能每新提一个问题前发送 propmt 命令他忘记 context)
        - https://github.com/jasonthewhale/Claude_In_Slack_API/blob/main/claude.py
    """
    prompt: str
    appid: Optional[str] = None
    token: Optional[str] = None