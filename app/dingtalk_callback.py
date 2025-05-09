import json
import dingtalk_stream

from app.config import Config
from app.open_web_ui_api import OpenWebUIApi
from app.prompt.observation import SYSTEM_PROMPT as OBSERVATION_SYSTEM_PROMPT
from loguru import logger
class DingtalkCallback(dingtalk_stream.GraphHandler):

    def __init__(self, config: Config, dingtalk_client: dingtalk_stream.DingTalkStreamClient):
        self.config = config
        self.logger = logger
        self.open_web_ui_api = OpenWebUIApi()
        self.dingtalk_client = dingtalk_client

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        request = dingtalk_stream.GraphRequest.from_dict(callback.data)
        self.logger.info('incoming request, method={}, uri={}, body={}',
                         request.request_line.method, request.request_line.uri,
                         request.body)
        payload = json.loads(request.body)
        react = True
        function_results = []
        messages = []
        messages.append({
            'role': 'user',
            'content': payload['rawInput']
        })
        while react:
            # function 选择
            function_name, function_args = await self.open_web_ui_api.choose_function(
                self.config.open_web_ui_model_name,
                payload['rawInput'],
                messages,
                payload['sessionWebhook']
            )
            if function_name and function_args:
                messages.append({
                    'role': 'assistant',
                    'content': f'function_call: {{"name": "{function_name}", "arguments": {function_args}}}'
                })
                logger.info('function selected function_name: {}, function_args: {}', function_name, function_args)
                # 调用 function
                function_result = await self.open_web_ui_api.invoke_function(function_name, function_args, payload['sessionWebhook'])
                if function_result:
                    messages.append({
                        'role': 'tool',
                        'content': function_result
                    })
                    function_results.append(function_result)
            else:
                react = False
                logger.info('no function selected')
            # 先加上防止死循环  需要调试react prompt才行
            # react = False
        # system prompt
        messages = []
        if function_results and len(function_results) > 0:
            messages.append({
                'role': 'system',
                'content': OBSERVATION_SYSTEM_PROMPT.replace('{{function_results}}', json.dumps(function_results))
            })
        messages.append({
            'role': 'user',
            'content': payload['rawInput']
        })
        await self.open_web_ui_api.chat_with_model_stream(
            self.config.open_web_ui_model_name,
            messages,
            payload['sessionWebhook']
        )
        
        response = self.get_success_response()
        return dingtalk_stream.AckMessage.STATUS_OK, response.to_dict()

    def get_success_response(self):
        response = dingtalk_stream.GraphResponse()
        response.status_line.code = 200
        response.status_line.reason_phrase = 'OK'
        response.headers['Content-Type'] = 'application/json'
        response.body = json.dumps({}, ensure_ascii=False)
        return response
