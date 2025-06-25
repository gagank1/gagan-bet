import asyncio
from httpx import AsyncClient
import os
import json
import time
import hashlib
import hmac
import base64
import uuid

class SwitchbotException(Exception):
    pass

class SwitchbotClient:
    def __init__(self, http_client: AsyncClient):
        self.client = http_client
        self.token = os.environ['SWITCHBOT_API_TOKEN']
        self.secret = os.environ['SWITCHBOT_SECRET_KEY']
    
    def get_headers(self):
        '''
        Get the headers for the Switchbot API.
        Returns a dictionary of the headers.
        '''
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

    async def get_all_devices(self, device_type: str | None = None):
        '''
        Get all devices from the Switchbot API.
        If device_type is provided, only return devices of that type.
        Returns a list of devices.
        '''
        response = await self.client.get('/v1.1/devices', headers=self.get_headers())
        response.raise_for_status()
        if response.json()['statusCode'] > 100:
            raise SwitchbotException(response.json()['message'])
        
        devices = response.json()['body']['deviceList']
        if device_type is not None:
            devices = [device for device in devices if device['deviceType'] == device_type]
        return devices
    
    async def get_device_status(self, device_id: str):
        '''
        Get the status of a device from the Switchbot API.
        Returns a dictionary of the device's status.
        '''
        response = await self.client.get(f'/v1.1/devices/{device_id}/status', headers=self.get_headers())
        response.raise_for_status()
        if response.json()['statusCode'] > 100:
            raise SwitchbotException(response.json()['message'])
        return response.json()['body']
    
    async def press_bot(self, device_id: str | None = None):
        '''
        Press the bot button.
        If device_id is not provided, use the device_id from the environment variable SWITCHBOT_DEVICE_ID.
        If multiple bot devices are found, raise an error.
        Returns a dictionary of the response.
        '''
        device_id = os.getenv('SWITCHBOT_DEVICE_ID', device_id)
        if device_id is None:
            # try to infer the device_id by fetching all bot devices
            devices = await self.get_all_devices(device_type='Bot')
            if len(devices) == 1:
                device_id = devices[0]['deviceId']
            elif len(devices) > 1:
                raise ValueError('Multiple bot devices found, cannot infer device_id. Please specify the device_id or set SWITCHBOT_DEVICE_ID.')
            else:
                raise ValueError('No bot devices found. Please specify device_id or set SWITCHBOT_DEVICE_ID.')
        
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
            raise SwitchbotException(response.json()['message'])
        return response.json()
