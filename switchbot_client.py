from httpx import AsyncClient
import os
import json
import time
import hashlib
import hmac
import base64
import uuid

class SwitchbotClient:
    def __init__(self, http_client: AsyncClient):
        self.client = http_client
        self.token = os.environ['SWITCHBOT_API_TOKEN']
        self.secret = os.environ['SWITCHBOT_SECRET_KEY']
        self.headers = self.get_headers()
    
    def get_headers(self):
        apiHeader = {}
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self.secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        print ('Authorization: {}'.format(self.token))
        print ('t: {}'.format(t))
        print ('sign: {}'.format(str(sign, 'utf-8')))
        print ('nonce: {}'.format(nonce))

        #Build api header JSON
        apiHeader['Authorization']=self.token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)
        return apiHeader

    async def get_devices(self):
        response = await self.client.get("/devices")
        return response.json()
