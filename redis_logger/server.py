from flask import Flask, jsonify, request, json, send_file, redirect, url_for, request,render_template
import re
import redis
from os import remove
import numpy as np
import time


app = Flask(__name__)

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

# To get it running....
# set FLASK_APP=estimation_server.py (windows)
# export FLASK_APP=estimation_server.py (linux)
# flask run --host=0.0.0.0 --port 80 (So it is externally visible on ip and on web port 80)
# flask run (only viewable on the localhost, defaults to port 5000)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    content = request.get_json()

    pipe = redis_conn.pipeline()
    model_id = int(redis_conn.get('model_id'))
    key = 'model' + ':' + str(model_id) + ':'
    pipe.rpush(key + 'method', content['method'])
    pipe.rpush(key + 'etime', content['etime'])
    pipe.rpush(key + 'mtotal', content['mtotal'])
    pipe.rpush(key + 'mfree', content['mfree'])
    pipe.rpush(key + 'mpercent', content['mpercent'])
    pipe.rpush(key + 'host', content['host'])
    pipe.rpush(key + 'tnow', time.time())
    pipe.execute()
    return "OK"

@app.route('/subblock', methods=['POST'])
def log_subblock():
    content = request.get_json()
    jobid = content['jobid']

    key = jobid
    redis_conn.rpush(key, time.time())
    return "OK"

@app.route('/nblock', methods=['POST'])
def log_nblock():
    content = request.get_json()
    nblocks = content['nblocks']
    redis_conn.rpush('nblocks', nblocks)
    return "OK"

@app.route('/init', methods=['GET','POST'])
def init():
    redis_conn.incr('model_id')
    return 'OK'

@app.route('/clear', methods=['POST'])
def clear():
    for key in redis_conn.keys():
        redis_conn.delete(key)

    return "OK"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1000, debug=True)
