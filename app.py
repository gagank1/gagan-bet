from flask import Flask, render_template, request, jsonify, redirect
import redis
import os
import json

app = Flask(__name__, static_url_path='/', static_folder='frontend/build')

# Sets up redis, set keys from docker compose environment variables
rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)
rdb.set('PRIVATE_PASSPHRASE', os.environ['PRIVATE_KEY'])
rdb.set('PUBLIC_PASSPHRASE', os.environ['INIT_PUBLIC_KEY'])


# Serve the React app
@app.route('/')
def index():
    return redirect('/index.html')

# Handle buzz in request
@app.route('/buzzin', methods=['POST'])
def buzzin():
    passphrase = request.form['public_passphrase']
    pwd = rdb.get('PUBLIC_PASSPHRASE')
    
    if passphrase == pwd:
        rdb.publish('BUZZ', json.dumps({
            'buzz': 'in'
        }))
        return "Buzzed in successfully"
    else:
        return ("Wrong passphrase", 401)

# Handle public passphrase update
@app.route('/updatepublickey', methods=['POST'])
def updatepublickey():
    entered_private_key = request.form['private_passphrase']
    true_private_key = rdb.get('PRIVATE_PASSPHRASE')
    
    if entered_private_key == true_private_key:
        new_public_key = request.form['new_public_passphrase']
        rdb.set('PUBLIC_PASSPHRASE', new_public_key)
        return "Successfully changed public passphrase"
    else:
        return ("Incorrect private passphrase", 401)

if __name__ == '__main__':
    app.run(debug=True)
