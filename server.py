# coding: utf-8


# third party
from flask import Flask, jsonify
from flask import request
from flask.ext.cors import CORS
import redis

# local
from config import redis_url

app = Flask(__name__)
app.debug = True
CORS(app)

redis = redis.from_url(redis_url)


print "Starting ReMind backend."


@app.route('/add', methods=["GET", "POST", "OPTIONS"])
def add_api():
    print "add called"
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        note = json["note"]
        redis.lpush('notes', note)
        return 'added'
    else:
        print "In non-POST block"
        return ''


@app.route('/remove_top')
def remove_top_api():
    print "remove top called"
    redis.lpop('notes')
    return 'remove_top'


@app.route('/list')
def list_api():
    print "list called"
    result = redis.lrange('notes', 0, 100)
    json = jsonify(notes=result)
    return json


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
