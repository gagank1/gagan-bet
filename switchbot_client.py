import asyncio
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
    
    def get_headers(self):
        apiHeader = {}
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self.secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        #Build api header JSON
        apiHeader['Authorization']=self.token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)
        return apiHeader

    async def get_all_devices(self):
        response = await self.client.get('/v1.1/devices', headers=self.get_headers())
        response.raise_for_status()
        if response.json()['statusCode'] > 100:
            raise ValueError(response.json()['message'])
        return response.json()
    
    async def press_bot(self, device_id: str | None = None):
        device_id = os.getenv('SWITCHBOT_DEVICE_ID', device_id)
        if device_id is None:
            raise ValueError('SWITCHBOT_DEVICE_ID is not set and no device_id was provided. one of these must be set')
        
        response = await self.client.post(
            f'/v1.1/devices/{device_id}/commands',
            headers=self.get_headers(),
            json={
                "command": "press",
                "parameter": "default",
                "commandType": "command"
            }
        )
        response.raise_for_status()
        if response.json()['statusCode'] > 100:
            raise ValueError(response.json()['message'])
        return response.json()
    
    async def boof_call(self):
        await asyncio.sleep(0.5)
