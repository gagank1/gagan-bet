import redis
import requests
import json
import traceback
import logging

logging.basicConfig(level=logging.INFO)

def run():
    rdb = redis.Redis(host='redis', port=6379, decode_responses=True)
    p = rdb.pubsub(ignore_subscribe_messages=True)
    p.subscribe('BUZZ')
    logging.info('Subscribed to BUZZ channel')
    
    try:
        for message in p.listen():
            d = message['data']
            d_dict = json.loads(d)
            logging.info(f'Got message: {d}')
    except Exception as e:
        p.close()
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    run()
