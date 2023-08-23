from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

import redis
import os
import logging
import asyncio
from typing import Annotated


app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/build'))

global_logger = logging.getLogger('uvicorn.error')
async def get_global_logger():
    return global_logger

rdb = redis.Redis(host='redis', port=6379, decode_responses=True)
async def get_rdb():
    return rdb

# load private/public keys from previous run if available
if rdb.exists('PRIVATE_PASSPHRASE') == 0:
    rdb.set('PRIVATE_PASSPHRASE', os.environ['PRIVATE_KEY'])
    global_logger.info(f'PRIVATE_PASSPHRASE initialized to {os.environ["PRIVATE_KEY"]}')
else:
    global_logger.info(f'PRIVATE_PASSPHRASE found: {rdb.get("PRIVATE_PASSPHRASE")}')

if rdb.exists('PUBLIC_PASSPHRASE') == 0:
    rdb.set('PUBLIC_PASSPHRASE', os.environ['INIT_PUBLIC_KEY'])
    global_logger.info(f'PUBLIC_PASSPHRASE initialized to {os.environ["INIT_PUBLIC_KEY"]}')
else:
    global_logger.info(f'PUBLIC_PASSPHRASE found: {rdb.get("PUBLIC_PASSPHRASE")}')

async def switchbot_api_call():
    await asyncio.sleep(1)
    # TODO: make call to switchbot api using httpx here

# Serve the React app
@app.get('/')
async def index(logger: Annotated[logging.Logger, Depends(get_global_logger)]):
    logger.debug('Hit /, redirecting to /static/index.html')
    return RedirectResponse('/static/index.html')

class BuzzinForm(BaseModel):
    public_passphrase: str

# Handle buzz in request
@app.post('/buzzin')
async def buzzin(bf: BuzzinForm, 
                 logger: Annotated[logging.Logger, Depends(get_global_logger)], 
                 client: Annotated['redis.Redis[str]', Depends(get_rdb)]):
    
    logger.info(f'Hit /buzzin, request: {bf.model_dump_json()}')
    
    passphrase = bf.public_passphrase
    pwd = client.get('PUBLIC_PASSPHRASE')
    
    if passphrase == pwd:
        await switchbot_api_call()
        logger.info('Buzzed in successfully')
        return {'message': 'Buzzed in successfully'}
    else:
        logger.error('Buzz in failed: wrong passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Wrong passphrase"}
        )

class PasswordChangeForm(BaseModel):
    private_passphrase: str
    new_public_passphrase: str

# Handle public passphrase update
@app.post('/updatepublickey')
async def updatepublickey(pcf: PasswordChangeForm, 
                 logger: Annotated[logging.Logger, Depends(get_global_logger)], 
                 client: Annotated['redis.Redis[str]', Depends(get_rdb)]):
    
    logger.info(f'Hit /updatepublickey, request: {pcf.model_dump_json()}')
    
    entered_private_key = pcf.private_passphrase
    true_private_key = client.get('PRIVATE_PASSPHRASE')
    
    if entered_private_key == true_private_key:
        new_public_key = pcf.new_public_passphrase
        client.set('PUBLIC_PASSPHRASE', new_public_key)
        logger.info(f'Updated public passphrase to {new_public_key}')
        return {'message': "Successfully changed public passphrase"}
    else:
        logger.error('Failed to set new public passphrase, incorrect private passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Incorrect private passphrase"}
        )
