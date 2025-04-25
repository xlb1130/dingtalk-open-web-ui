
from loguru import logger
from app.dingtalk_client import DingtalkClient
    
def main():
    logger.info('start dingtalk open web ui ...')
    client = DingtalkClient()
    client.run()

if __name__ == '__main__':
    main()