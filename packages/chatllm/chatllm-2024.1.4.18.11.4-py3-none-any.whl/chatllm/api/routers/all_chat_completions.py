#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/12/19 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from sse_starlette import EventSourceResponse
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.llmchain.completions import github_copilot
from chatllm.llmchain.completions import moonshot_kimi
from chatllm.llmchain.completions import deepseek
from chatllm.llmchain.applications import ChatFiles

from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]

send_message = lru_cache(send_message)


@router.post("/chat/completions")
def chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    logger.debug(request)

    api_key = auth and auth.credentials or None
    logger.debug(api_key)

    model = request.model.strip().lower()
    data = request.model_dump()

    ############################################################################
    if model.startswith(('rag', 'chatfile')):  # rag-, chatfile-, chatfiles-
        model = '-' in model and model.split('-', 1)[1] or "gpt-3.5-turbo"
        # todo: rag结构体
        # request.rag

        response = (
            ChatFiles(model=model, openai_api_key=api_key, stream=data.get('stream'))
            .load_file(file=io.BytesIO(request.rag.get('file', b'')))
            .create_sse(query=data.get('messages')[-1].get('content')))

        return response

    ############################################################################

    if model.startswith(('kimi', 'moonshot')):
        if any(i in model for i in ('web', 'search', 'net')):
            data['use_search'] = True  # 联网模型

        completions = moonshot_kimi.Completions(api_key=api_key)

    elif model.startswith(('deepseek',)):
        completions = deepseek.Completions(api_key=api_key)

    else:  # todo: 兜底
        completions = github_copilot.Completions(api_key=api_key)  # OpenAI().completions
        send_message(api_key, title="github_copilot", n=3)

    response: ChatCompletionResponse = completions.create_sse(**data)
    return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
