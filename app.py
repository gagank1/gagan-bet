from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import secrets
import datetime
import json

import os
import logging
import asyncio
from typing import Annotated
import redis.asyncio as redis

# Redis connection
redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)

async def get_db():
    return redis_client

app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/build'))

global_logger = logging.getLogger('uvicorn.error')
async def get_global_logger():
    return global_logger


async def switchbot_api_call():
    await asyncio.sleep(0.5)
    # TODO: make call to switchbot api using httpx here


# Serve the React app
@app.get('/')
async def index(logger: Annotated[logging.Logger, Depends(get_global_logger)]):
    logger.debug('Hit /, serving index.html')
    return FileResponse('frontend/build/index.html')

async def get_redis_value(
    key: str,
    redis_client: redis.Redis,
    logger: logging.Logger,
):
    value = await redis_client.get(key)
    
    if value is not None:
        return value
    else:
        logger.error(f'Could not read key "{key}" from Redis')
        raise ValueError(f'Redis error: could not find key "{key}"')


class BuzzinForm(BaseModel):
    public_passphrase: str

# Handle buzz in request
@app.post('/buzzin')
async def buzzin(bf: BuzzinForm, 
                 logger: Annotated[logging.Logger, Depends(get_global_logger)], 
                 redis_client: Annotated[redis.Redis, Depends(get_db)]):
    
    logger.info(f'Hit /buzzin, request: {bf.model_dump_json()}')
    
    passphrase = bf.public_passphrase
    
    pwd = await get_redis_value('public_passphrase', redis_client, logger)
    
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
                          redis_client: Annotated[redis.Redis, Depends(get_db)]):
    
    logger.info(f'Hit /updatepublickey, request: {pcf.model_dump_json()}')
    
    entered_private_key = pcf.private_passphrase
    true_private_key = await get_redis_value('private_passphrase', redis_client, logger)
    
    if entered_private_key == true_private_key:
        new_public_key = pcf.new_public_passphrase
        await redis_client.set('public_passphrase', new_public_key)
        logger.info(f'Updated public passphrase to {new_public_key}')
        return {'message': "Successfully changed public passphrase"}
    else:
        logger.error('Failed to set new public passphrase, incorrect private passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Incorrect private passphrase"}
        )

class CreateTempKeyForm(BaseModel):
    private_passphrase: str
    expiration_hours: int = 24  # Default to 24 hours if not specified
    max_uses: int = 1  # Default to single use
    note: str = ""  # Optional note/label for the key

class TempKeyInfo(BaseModel):
    key: str
    created_at: str
    expires_at: str
    remaining_uses: int
    note: str

@app.post('/createtempkey')
async def create_temp_key(
    form: CreateTempKeyForm,
    logger: Annotated[logging.Logger, Depends(get_global_logger)],
    redis_client: Annotated[redis.Redis, Depends(get_db)]
):
    logger.info(f'Hit /createtempkey, request: {form.model_dump_json()}')
    
    # Verify private passphrase
    entered_private_key = form.private_passphrase
    true_private_key = await get_redis_value('private_passphrase', redis_client, logger)
    
    if entered_private_key != true_private_key:
        logger.error('Failed to create temp key: incorrect private passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Incorrect private passphrase"}
        )
    
    # Generate a random key
    temp_key = secrets.token_urlsafe(16)
    
    # Store in Redis with expiration
    expiration_seconds = form.expiration_hours * 3600
    created_at = datetime.datetime.now().isoformat()
    expires_at = (datetime.datetime.now() + datetime.timedelta(hours=form.expiration_hours)).isoformat()
    
    # Store key info as a JSON string
    key_info = {
        'remaining_uses': form.max_uses,
        'note': form.note,
        'created_at': created_at,
        'expires_at': expires_at
    }
    
    await redis_client.set(f'temp_key:{temp_key}', json.dumps(key_info), ex=expiration_seconds)
    
    logger.info(f'Created temporary key that expires in {form.expiration_hours} hours with {form.max_uses} uses')
    return {
        'message': 'Temporary key created successfully',
        'temp_key': temp_key,
        'expires_in_hours': form.expiration_hours,
        'max_uses': form.max_uses,
        'note': form.note
    }

@app.get('/tempkey/{temp_key}')
async def use_temp_key(
    temp_key: str,
    logger: Annotated[logging.Logger, Depends(get_global_logger)],
    redis_client: Annotated[redis.Redis, Depends(get_db)]
):
    logger.info(f'Hit /tempkey/{temp_key}')
    
    # Get key info
    key_info_str = await redis_client.get(f'temp_key:{temp_key}')
    
    if not key_info_str:
        logger.error(f'Invalid or expired temporary key: {temp_key}')
        return JSONResponse(
            status_code=401,
            content={'message': "Invalid or expired temporary key"}
        )
    
    # Parse key info
    key_info = json.loads(key_info_str)
    remaining_uses = key_info['remaining_uses']
    
    if remaining_uses <= 0:
        logger.error(f'Temporary key has no remaining uses: {temp_key}')
        return JSONResponse(
            status_code=401,
            content={'message': "Temporary key has no remaining uses"}
        )
    
    # Decrement remaining uses
    key_info['remaining_uses'] = remaining_uses - 1
    ttl = await redis_client.ttl(f'temp_key:{temp_key}')
    
    # Update key info in Redis
    if key_info['remaining_uses'] > 0:
        await redis_client.set(f'temp_key:{temp_key}', json.dumps(key_info), ex=ttl)
    else:
        # Delete key if no uses remaining
        await redis_client.delete(f'temp_key:{temp_key}')
    
    # Trigger the buzzer
    await switchbot_api_call()
    logger.info('Buzzed in successfully with temporary key')
    return {'message': 'Buzzed in successfully'}

@app.get('/listtempkeys')
async def list_temp_keys(
    private_passphrase: str,
    logger: Annotated[logging.Logger, Depends(get_global_logger)],
    redis_client: Annotated[redis.Redis, Depends(get_db)]
):
    logger.info('Hit /listtempkeys')
    
    # Verify private passphrase
    true_private_key = await get_redis_value('private_passphrase', redis_client, logger)
    
    if private_passphrase != true_private_key:
        logger.error('Failed to list temp keys: incorrect private passphrase')
        return JSONResponse(
            status_code=401,
            content={'message': "Incorrect private passphrase"}
        )
    
    # Get all temp keys
    keys = await redis_client.keys('temp_key:*')
    active_keys = []
    
    for key in keys:
        key_info_str = await redis_client.get(key)
        if key_info_str:
            key_info = json.loads(key_info_str)
            temp_key = key.replace('temp_key:', '')
            active_keys.append(TempKeyInfo(
                key=temp_key,
                created_at=key_info['created_at'],
                expires_at=key_info['expires_at'],
                remaining_uses=key_info['remaining_uses'],
                note=key_info['note']
            ))
    
    return {'active_keys': active_keys}

@app.get('/validatetempkey/{temp_key}')
async def validate_temp_key(
    temp_key: str,
    logger: Annotated[logging.Logger, Depends(get_global_logger)],
    redis_client: Annotated[redis.Redis, Depends(get_db)]
):
    logger.info(f'Hit /validatetempkey/{temp_key}')
    
    # Get key info
    key_info_str = await redis_client.get(f'temp_key:{temp_key}')
    
    if not key_info_str:
        logger.error(f'Invalid or expired temporary key: {temp_key}')
        return JSONResponse(
            status_code=401,
            content={'message': "Invalid or expired temporary key"}
        )
    
    # Parse key info
    key_info = json.loads(key_info_str)
    remaining_uses = key_info['remaining_uses']
    
    if remaining_uses <= 0:
        logger.error(f'Temporary key has no remaining uses: {temp_key}')
        return JSONResponse(
            status_code=401,
            content={'message': "Temporary key has no remaining uses"}
        )
    
    return {
        'message': 'Valid temporary key',
        'remaining_uses': remaining_uses,
        'expires_at': key_info['expires_at']
    }

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Skip API routes
    if full_path.startswith(('tempkey/', 'createtempkey', 'listtempkeys', 'buzzin', 'updatepublickey')):
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Serve static files if they exist
    static_path = os.path.join("frontend/build", full_path)
    if os.path.exists(static_path) and os.path.isfile(static_path):
        return FileResponse(static_path)
    
    # Otherwise serve index.html
    return FileResponse("frontend/build/index.html")
