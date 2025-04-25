import json
import requests
import dingtalk_stream
from loguru import logger
from app.config import config

class OpenWebUIApi:
    
    def __init__(self):
        self.logger = logger
    
    async def chat_with_model_stream(
        self,
        model_name: str,
        messages: list,
        webhook: str,
        dingtalk_client: dingtalk_stream.DingTalkStreamClient,
        incoming_message: dingtalk_stream.ChatbotMessage,
        files: list = []
    ):
        payload = {
            "model": model_name,
            "messages": messages,
            "files": files,
            "stream": True
        }
        headers = {
            'Authorization': f'Bearer {config.open_web_ui_api_key}'
        }
        logger.info(f'Sending messags to Open Web UI API, payload: {payload}')
        try:
            with requests.post(
                f'{config.open_web_ui_host}/api/chat/completions',
                headers=headers,
                json=payload,
                stream=True,
                timeout=config.open_web_ui_api_timeout
            ) as response:
                content = ''
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        # logger.info(f'Received message from Open Web UI API: {line}')
                        if line.startswith('data:') and 'content' in line:
                            content += json.loads(line.lstrip('data:'))['choices'][0]['delta']['content']
                            self.reply_markdown(webhook=webhook, content=content)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f'Error sending messages to Open Web UI API: {e}')
            raise e
        
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
    