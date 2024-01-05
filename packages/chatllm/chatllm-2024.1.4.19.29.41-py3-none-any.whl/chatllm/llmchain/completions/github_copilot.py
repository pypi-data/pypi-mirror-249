#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 不准白嫖 必须 star, todo: 位置错误结构体

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue
from meutils.async_utils import sync_to_async
from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from chatllm.schemas.openai_types import chat_completion_error, chat_completion_chunk_error

requests.post = retrying(requests.post)

GITHUB_BASE_URL = os.getenv('GITHUB_BASE_URL', 'https://api.github.com')
GITHUB_COPILOT_BASE_URL = os.getenv('GITHUB_COPILOT_BASE_URL', 'https://api.githubcopilot.com')


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(self.api_key)

    def create(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):  # ChatCompletionRequest: 定义请求体

        data = {
            "model": 'gpt-4',
            "messages": messages if isinstance(messages, list) else [{"role": "user", "content": messages}],
            **kwargs
        }

        # logger.debug(data)

        if data.get('stream'):
            interval = 0.05 if "gpt-4" in data['model'] else 0.01
            return self.smooth_stream(interval=interval, **data)
        else:
            return self._create(**data)

    def create_sse(self, **data):
        response = self.create(**data)
        if data.get('stream'):
            from sse_starlette import EventSourceResponse
            generator = (chunk.model_dump_json() for chunk in response)
            return EventSourceResponse(generator, ping=10000)
        return response

    @sync_to_async(thread_sensitive=False)
    def acreate(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):
        """
            generator = (chunk.model_dump_json() for chunk in completions.acreate(messages)
        """
        return self.create(messages, **kwargs)

    def _create(self, **data):
        response = self._post(**data)
        if response.status_code != 200:
            chat_completion_error.choices[0].message.content = response.text
            return chat_completion_error

        response = response.json()
        response['model'] = data.get('model', 'gpt-4')
        response['object'] = 'chat.completion'
        response['choices'][0]['logprobs'] = None

        # ChatCompletion.choices[0].logprobs = None
        return ChatCompletion.model_validate(response)

    def _stream_create(self, **data):
        response = self._post(**data)
        # logger.debug(response.text)

        if response.status_code != 200:
            chat_completion_chunk_error.choices[0].delta.content = response.text
            yield chat_completion_chunk_error
            return

        for chunk in response.iter_lines(chunk_size=1024):
            if chunk and chunk != b'data: [DONE]':
                # logger.debug(chunk)

                chunk = chunk.strip(b"data: ")
                chunk = json.loads(chunk)
                chunk['model'] = data.get('model', "gpt-4")
                chunk['object'] = "chat.completion.chunk"
                chunk['choices'][0]['finish_reason'] = chunk['choices'][0].get('finish_reason')  # 最后为 "stop"
                chunk = ChatCompletionChunk.model_validate(chunk)

                chunk.choices[0].delta.role = 'assistant'
                content = chunk.choices[0].delta.content or ''
                chunk.choices[0].delta.content = content

                if content or chunk.choices[0].finish_reason:
                    # logger.debug(chunk)
                    yield chunk

                # content_filter
                if chunk.choices[0].finish_reason == "content_filter":
                    title = "OPENAI: CONTENT_FILTER"
                    send_message(title=title, content=str(data))

                    # chat_completion_chunk_error.choices[0].delta.content = title
                    # yield chat_completion_chunk_error

    def _post(self, **data):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            # 'X-Request-Id': str(uuid.uuid4()),
            # 'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
            # 'vscode-machineid': machine_id,
            'Editor-Version': 'vscode/1.84.2',
            'Editor-Plugin-Version': 'copilot-chat/0.10.2',
            'Openai-Organization': 'github-copilot',
            'Openai-Intent': 'conversation-panel',
            'Content-Type': 'application/json',
            'User-Agent': 'GitHubCopilotChat/0.10.2',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        url: str = f"{GITHUB_COPILOT_BASE_URL}/chat/completions"
        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=data.get('stream')
        )
        # logger.debug(response.status_code) # 400 # bad request: Authorization header is badly formatted

        if response.status_code != 200:
            send_message(title=self.__class__.__name__, content=f"{response.text}\n\n{self.api_key}")

        return response

    @staticmethod
    @retrying
    @ttl_cache(ttl=15 * 60)  # 1500
    def get_access_token(api_key: Optional[str] = None):
        """
        {
        'annotations_enabled': True,
        'chat_enabled': True,
        'chat_jetbrains_enabled': False,
        'code_quote_enabled': True,
        'copilot_ide_agent_chat_gpt4_small_prompt': False,
        'copilotignore_enabled': False,
        'expires_at': 1703653893,
        'intellij_editor_fetcher': False,
        'prompt_8k': True,
        'public_suggestions': 'disabled',
        'refresh_in': 1500,
        'sku': 'yearly_subscriber',
        'snippy_load_test_enabled': False,
        'telemetry': 'enabled',
        'token': 'tid=925df46f15a3245bfa77d9f47cc073e1;exp=1703653893;sku=yearly_subscriber;st=dotcom;chat=1;rt=1;8kp=1:d5aeff67b9daa42231871e2434ad17152c6e0a68f685fa630e1bae1148283964',
        'tracking_id': '925df46f15a3245bfa77d9f47cc073e1',
        'vsc_panel_v2': False
        }
        {
            "annotations_enabled": true,
            "chat_enabled": true,
            "chat_jetbrains_enabled": false,
            "code_quote_enabled": false,
            "copilot_ide_agent_chat_gpt4_small_prompt": false,
            "copilotignore_enabled": false,
            "expires_at": 1702022150,
            "prompt_8k": true,
            "public_suggestions": "enabled",
            "refresh_in": 1500,
            "sku": "free_educational",
            "snippy_load_test_enabled": false,
            "telemetry": "enabled",
            "token": "tid=74069a4394491f4f41fc74888f24a0ab;exp=1702022150;sku=free_educational;st=dotcom;chat=1;sn=1;rt=1;8kp=1:b78c67b8a5d886b71b13a956f378d9b955299e5ad156a5699ab12cbeb5e7b960",
            "tracking_id": "74069a4394491f4f41fc74888f24a0ab",
            "vsc_panel_v2": false
        }
        """
        api_key = api_key or os.getenv("GITHUB_COPILOT_TOKEN")
        assert api_key

        headers = {
            'Host': 'api.github.com',
            'authorization': f'token {api_key}',
            "Editor-Version": "vscode/1.84.2",
            "Editor-Plugin-Version": "copilot/1.138.0",
            "User-Agent": "GithubCopilot/1.138.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        url = f"{GITHUB_BASE_URL}/copilot_internal/v2/token"
        response = requests.get(url, headers=headers)

        return response.json().get('token')  # response.get('error_details') 监控到 token 失效，返回 error_details，半小时过期

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason

    def smooth_stream(self, interval: Optional[float] = None, **data):
        stream = self._stream_create(**data)
        if interval:
            stream = UniformQueue(stream).consumer(interval=interval, break_fn=self.break_fn)
        return stream

    @classmethod
    def chat(cls, data: dict):  # TEST
        """
            Completions.chat(data)
        """
        with timer('聊天测试'):
            _ = cls().create(**data)

            print(f'{"-" * 88}\n')
            if isinstance(_, Generator):
                for i in _:
                    content = i.choices[0].delta.content
                    print(content, end='')
            else:
                print(_.choices[0].message.content)
            print(f'\n\n{"-" * 88}')


if __name__ == '__main__':
    # 触发风控
    s = """
    Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”管道细长、阻力太大时的轴向柱塞泵故障如何解决？“,输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
['排故方法']

Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”转向缸出现爬行现象，但是压力表却忽高忽低，相对应的解决方案是？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
['原因分析']、['排故方法']

Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”在模拟训练场A，轴向柱塞马达出现过什么故障？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。

['故障现象']

已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”密封圈挤出间隙的解决方法是什么？“。输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
    """

    s = "讲个故事"
    # s = '树上9只鸟，打掉1只，还剩几只'

    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': "你是gpt4, Let's think things through one step at a time."},
            {'role': 'user', 'content': s}
        ],
        'stream': True}

    Completions.chat(data)

    # async def main():
    #     _ = await Completions().acreate(**data)
    #
    #     content = ''
    #     for i in _:
    #         content += i.choices[0].delta.content
    #     return content
    #
    #
    # print(arun(main()))

    # with timer('异步'):
    #     print([Completions().acreate(**data) for _ in range(10)] | xAsyncio)

    # data = {
    #     'model': 'gpt-xxx',
    #     'messages': [{'role': 'user', 'content': '讲个故事。 要足够长，这对我很重要。'}],
    #     'stream': False,
    #     # 'max_tokens': 16000
    # }
    # data = {
    #     'model': 'gpt-4',
    #     'messages': '树上9只鸟，打掉1只，还剩几只',  # [{'role': 'user', 'content': '树上9只鸟，打掉1只，还剩几只'}],
    #     'stream': False,
    #     'temperature': 0,
    #     # 'max_tokens': 32000
    # }
    #
    # for i in tqdm(range(1000)):
    #     _ = Completions().create(**data)
    #     print(_.choices[0].message.content)
    #     break
