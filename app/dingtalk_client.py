import dingtalk_stream
from app.config import Config
from app.dingtalk_callback import DingtalkCallback

class DingtalkClient(object):
    def __init__(self):
        self.config = Config()

    def run(self):
        credential = dingtalk_stream.Credential(self.config.dingtalk_client_id, self.config.dingtalk_client_secret)
        client = dingtalk_stream.DingTalkStreamClient(credential)
        client.register_callback_handler(dingtalk_stream.graph.GraphMessage.TOPIC, DingtalkCallback(self.config, client))
        client.start_forever()