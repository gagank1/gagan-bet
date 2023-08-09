import redis
import requests
import json
import traceback
import logging

def run():
    rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)
    p = rdb.pubsub(ignore_subscribe_messages=True)
    p.subscribe('BUZZ')
    
    try:
        for message in p.listen():
            d: bytes = message['data']
            d_dict = json.loads(d.decode())
            print(f'Got message: {d_dict}')
    except Exception as e:
        p.close()
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    run()
