#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2023/12/19 09:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.completion_create_params import CompletionCreateParams


class SpeechCreateRequest(BaseModel):
    input: str
    model: str = 'tts'
    voice: str = "alloy"
    response_format: Literal["mp3", "opus", "aac", "flac"] = "mp3"
    speed: float = 1


chat_completion = {
    "id": "chatcmpl-id",
    "object": "chat.completion",
    "created": 0,
    "model": "LLM",
    "choices": [
        {
            "message": {"role": "assistant", "content": ''},
            "index": 0,
            "finish_reason": "stop",
            "logprobs": None
        }
    ],
    "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

}

chat_completion_chunk = {
    "id": "chatcmpl-id",
    "object": "chat.completion.chunk",
    "created": 0,
    "model": "LLM",
    "choices": [
        {
            "delta": {"role": "assistant", "content": ''},
            "index": 0,
            "finish_reason": "stop",
            "logprobs": None
        }
    ]
}

# 通用
chat_completion = ChatCompletion.model_validate(chat_completion)
chat_completion_chunk = ChatCompletionChunk.model_validate(chat_completion_chunk)

# ONEAPI_SLOGAN
ONEAPI_SLOGAN = os.getenv("ONEAPI_SLOGAN", "\n\n[永远相信美好的事情即将发生](https://api.chatllm.vip/)")

chat_completion_slogan = chat_completion.model_copy(deep=True)
chat_completion_slogan.choices[0].message.content = ONEAPI_SLOGAN

chat_completion_chunk_slogan = chat_completion_chunk.model_copy(deep=True)
chat_completion_chunk_slogan.choices[0].delta.content = ONEAPI_SLOGAN

# ERROR
chat_completion_error = chat_completion.model_copy(deep=True)
chat_completion_chunk_error = chat_completion_chunk.model_copy(deep=True)


class ChatCompletionRequest(BaseModel):
    request: CompletionCreateParams = {}
    headers: dict = {}  # HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")


if __name__ == '__main__':
    # data = {"stream": True, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "你好"}]}
    # print(ChatCompletionRequest(request=data).request)
    # print(chat_completion_error)
    # print(chat_completion_slogan)

    pass
