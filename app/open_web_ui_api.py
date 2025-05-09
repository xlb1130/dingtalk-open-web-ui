import json
import requests
import dingtalk_stream
import app.util.open_api_util as open_api_util
from loguru import logger
from app.config import config
from app.prompt.function_call import SYSTEM_PROMPT as FUCNTION_SYSTEM_PROMPT
from app.prompt.function_call import USER_PROMPT as FUCNTION_USER_PROMPT

class OpenWebUIApi:
    
    def __init__(self):
        self.logger = logger
        self.settings = {}
        self.headers = {
            'Authorization': f'Bearer {config.open_web_ui_api_key}'
        }
        self.functions = {}
        self.init_settings()
        self.init_tools()
    
    def init_settings(self):
        # 获取 openwebui 的 settings
        self.settings = requests.get(
            f'{config.open_web_ui_host}/api/v1/users/user/settings',
            headers=self.headers,
            timeout=config.open_web_ui_api_timeout
        ).json()
        self.tool_servers = self.settings['ui']['toolServers']
        
    def init_tools(self):
        if not self.tool_servers: 
            return
        # 初始化 openwebui 的 tool servers
        for tool_server in self.tool_servers:
            open_api_result = requests.get(
                f'{tool_server['url']}/{tool_server["path"]}',
                headers=self.headers,
                timeout=config.open_web_ui_api_timeout
            )
            
            if 'openapi' in open_api_result.json():
                open_api_result = open_api_util.parse_openapi_json(tool_server['url'],open_api_result.json())
                for tool in open_api_result:
                    logger.info(f'function_name={tool["name"]}')
                    self.functions[tool['name']] = tool
            else:
                logger.error(f'{tool_server['url']}/{tool_server["path"]} result open_api_result={open_api_result.json()}')
                
    async def choose_function(
        self,
        model_name: str,
        user_input: str,
        history: list,
        webhook: str
    ):
        function_all = []
        for function_name, function in self.functions.items():
            function_all.append(function)
        payload = {
            "model": model_name,
            "messages": [
                {
                    'role': 'system', 
                    'content': FUCNTION_SYSTEM_PROMPT.replace('$$$functions$$$', json.dumps(function_all))
                },
                {
                    'role': 'user', 
                    'content': FUCNTION_USER_PROMPT.replace('$$$user_input$$$', user_input).replace('$$$history$$$', json.dumps(history))
                },
            ],
            "stream": False
        }
    
        try:
            response = requests.post(
                f'{config.open_web_ui_host}/api/chat/completions',
                headers=self.headers,
                json=payload,
                timeout=config.open_web_ui_api_timeout
            )
            result = response.json()['choices'][0]['message']['content']
            # {  "tool_calls": [    {"name": "tool_maps_direction_driving_post", "parameters": {"origin": "116.4074,39.9042", "destination": "106.2782,38.4689"}}  ]}
            tool_calls = json.loads(result)['tool_calls']
            if tool_calls and len(tool_calls) > 0:
                function_name = tool_calls[0]['name']
                function_args = tool_calls[0]['parameters']
                self.logger.info('function_name={}, function_args={}', function_name, function_args)
                return function_name, function_args
            self.logger.info('choose_function, webhook={}, response={}, payload={}', webhook, response.json(), payload)
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error sending messages to Open Web UI API: {e}')
            raise e
        return None, None
        
    async def chat_with_model_stream(
        self,
        model_name: str,
        messages: list,
        webhook: str,
        files: list = []
    ):
        payload = {
            "model": model_name,
            "messages": messages,
            "files": files,
            "stream": True
        }
        logger.info(f'Sending messags to Open Web UI API, payload: {payload}')
        try:
            with requests.post(
                f'{config.open_web_ui_host}/api/chat/completions',
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=config.open_web_ui_api_timeout
            ) as response:
                if response.status_code == 200:
                    content = ''
                    for line in response.iter_lines(decode_unicode=True):
                        logger.info(line)
                        if line:
                            # logger.info(f'Received message from Open Web UI API: {line}')
                            if line.startswith('data:') and 'content' in line:
                                content += json.loads(line.lstrip('data:'))['choices'][0]['delta']['content']
                                self.reply_markdown(webhook=webhook, content=content)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f'Error sending messages to Open Web UI API: {e}')
            raise e
    async def invoke_function(self, function_name, function_args, webhook):
        payload = function_args
        try:
            function = self.functions[function_name]
            response = requests.post(
                function['url'],
                json=payload,
            )
            self.logger.info('function_name={}, function_args={}, response={}, response.body={}', function_name, function_args, response, response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error invloke function: {function_name} with arguments: {function_args}, exception is {e}')
            return {f'Error invloke function: {function_name} with arguments: {function_args}, exception is {e.message}'}
        
    def reply_markdown(self, webhook, content):
        payload = {
            'contentType': 'ai_card',
            'content': {
                'templateId': config.dingtalk_template_card_id,
                'cardData': {
                    'markdown': content,
                }
            }
        }
        response = requests.post(webhook, json=payload)
        self.logger.info('agent reply, webhook={}, response={}, response.body={}, payload={}', webhook, response, response.json(), payload)
    
