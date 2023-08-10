from flask import Flask, render_template, request, jsonify, redirect
import redis
import os
import json
import logging

app = Flask(__name__, static_url_path='/', static_folder='frontend/build')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Sets up redis, set keys from docker compose environment variables
rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)
rdb.set('PRIVATE_PASSPHRASE', os.environ['PRIVATE_KEY'])
rdb.set('PUBLIC_PASSPHRASE', os.environ['INIT_PUBLIC_KEY'])


# Serve the React app
@app.route('/')
def index():
    app.logger.debug('Hit /, redirecting to /index.html')
    return redirect('/index.html')

# Handle buzz in request
@app.route('/buzzin', methods=['POST'])
def buzzin():
    app.logger.info(f'Hit /buzzin, request: {json.dumps(request.json)}')
    
    content = request.json
    passphrase = content['public_passphrase']
    pwd = rdb.get('PUBLIC_PASSPHRASE')
    
    if passphrase == pwd:
        rdb.publish('BUZZ', json.dumps({
            'buzz': 'in'
        }))
        return jsonify({'message': 'Buzzed in successfully'})
    else:
        return jsonify({'message': "Wrong passphrase"}), 401

# Handle public passphrase update
@app.route('/updatepublickey', methods=['POST'])
def updatepublickey():
    app.logger.info(f'Hit /updatepublickey, request: {json.dumps(request.json)}')
    content = request.json
    
    entered_private_key = content['private_passphrase']
    true_private_key = rdb.get('PRIVATE_PASSPHRASE')
    
    if entered_private_key == true_private_key:
        new_public_key = content['new_public_passphrase']
        rdb.set('PUBLIC_PASSPHRASE', new_public_key)
        return jsonify({'message': "Successfully changed public passphrase"})
    else:
        return jsonify({'message': "Incorrect private passphrase"}), 401

if __name__ == '__main__':
    app.run(debug=True)
