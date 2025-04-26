import dingtalk_stream
from loguru import logger

class CardBotHandler(dingtalk_stream.ChatbotHandler):
    def __init__(self):
        super(dingtalk_stream.ChatbotHandler, self).__init__()
        self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        """处理消息回调"""
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        self.logger.info(f"收到消息：{incoming_message}")

        # if incoming_message.message_type not in ["text", "picture", "richText"]:
        #     self.reply_text("俺只看得懂文字和图片喔~", incoming_message)
        #     return AckMessage.STATUS_OK, "OK"

        # # 创建异步任务处理消息
        # asyncio.create_task(handle_reply_and_update_card(self, incoming_message, callback.data))
        # return AckMessage.STATUS_OK, "OK"