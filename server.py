# coding: utf-8


# third party
from flask import Flask, jsonify, make_response
import redis

# local
from config import redis_url

app = Flask(__name__)
app.debug = True

redis = redis.from_url(redis_url)


def tmpresponse(o):
    response = make_response(o)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


count = 0


@app.route('/add')
def add_api():
    global count
    count += 1
    value = "test count=%d" % count
    redis.lpush('notes', value)
    return tmpresponse('added')


@app.route('/remove_top')
def remove_top_api():
    redis.lpop('notes')
    return tmpresponse('remove_top')


@app.route('/list')
def list_api():
    result = redis.lrange('notes', 0, 100)
    json = jsonify(notes=result)
    return tmpresponse(json)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
