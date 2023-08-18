import redis
import requests
import json
import traceback
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO)

rdb = redis.Redis(host='redis', port=6379, decode_responses=True)
p = rdb.pubsub(ignore_subscribe_messages=True)
p.subscribe('BUZZ')
logging.info('Subscribed to BUZZ channel')

# for faster shutdown on `docker compose down`
def graceful_shutdown(signum, frame):
    logging.info("Received SIGTERM signal. Shutting down...")
    p.close()
    sys.exit(0)
signal.signal(signal.SIGTERM, graceful_shutdown)

def run():
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
else:
    p.close()
