import json
import dingtalk_stream

from app.config import Config
from app.open_web_ui_api import OpenWebUIApi
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
        
        await self.open_web_ui_api.chat_with_model_stream(
            self.config.open_web_ui_model_name,
            [{'role': 'user', 'content': payload['rawInput']}],
            payload['sessionWebhook'],
            self.dingtalk_client,
            dingtalk_stream.ChatbotMessage.from_dict(callback.data)
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