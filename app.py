from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

import os
import logging
import asyncio
from typing import Annotated

from google.cloud import firestore

db = firestore.Client(project='buzzer-418603', database='passkeys')

async def get_db():
    return db

doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})


app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/build'))

global_logger = logging.getLogger('uvicorn.error')
async def get_global_logger():
    return global_logger


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
                 firestore: Annotated[firestore.Client, Depends(get_db)]):
    
    logger.info(f'Hit /buzzin, request: {bf.model_dump_json()}')
    
    passphrase = bf.public_passphrase
    pwd = 'mockpwd'
    
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
                 client: Annotated[firestore.Client, Depends(get_db)]):
    
    logger.info(f'Hit /updatepublickey, request: {pcf.model_dump_json()}')
    
    entered_private_key = pcf.private_passphrase
    true_private_key = 'mockprivatekey'
    
    if entered_private_key == true_private_key:
        new_public_key = pcf.new_public_passphrase
        # client.set('PUBLIC_PASSPHRASE', new_public_key)
        logger.info(f'Updated public passphrase to {new_public_key}')
        return {'message': "Successfully changed public passphrase"}
    else:
        logger.error('Failed to set new public passphrase, incorrect private passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Incorrect private passphrase"}
        )
