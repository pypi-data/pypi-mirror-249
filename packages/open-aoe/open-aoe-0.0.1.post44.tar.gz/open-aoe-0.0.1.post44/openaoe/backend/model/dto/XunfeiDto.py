from pydantic import BaseModel
from typing import Optional, List


class Header(BaseModel):
    # 应用appid，从开放平台控制台创建的应用中获取
    app_id: Optional[str] = None
    # 每个用户的id，用于区分不同用户, 最大长度32
    uid: Optional[str] = None


class Chat(BaseModel):
    # 指定访问的领域, 取值为 general
    domain: str = "generalv2"
    # 核采样阈值。用于决定结果随机性，取值越高随机性越强即相同的问题得到的不同答案的可能性越高, 取值为[0,1],默认为0.5
    temperature: Optional[float] = 0.5
    # 模型回答的tokens的最大长度, 取值为[1,4096]，默认为2048
    max_tokens: Optional[int] = 2048
    # 从k个候选中随机选择⼀个（⾮等概率）,取值为[1，6],默认为4
    top_k: Optional[int] = 4
    # 用于关联用户会话, 需要保障用户下的唯一性
    chat_id: Optional[str]


class Parameter(BaseModel):
    chat: Chat


class Text(BaseModel):
    # user表示是用户的问题，assistant表示AI的回复 [user, assistant]
    role: str
    # 用户和AI的对话内容,所有content的累计tokens需控制8192以内
    content: str


class Message(BaseModel):
    text: List[Text]


class Payload(BaseModel):
    message: Message


class XunfeiSparkChatReqDto(BaseModel):
    header: Optional[Header] = None
    parameter: Parameter
    payload: Payload
