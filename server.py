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


def redis_key_from_email(email):
    """Compute redis key from email adress
    E.g. olof.bjarnason@gmail.com:book"""
    return '%s:book' % email


@app.route('/add', methods=["GET", "POST", "OPTIONS"])
def add_api():
    print "add called"
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        note = json["note"]
        email = json["email"]
        redis.lpush(redis_key_from_email(email), note)
        return 'added'

    else:
        print "In non-POST block"
        return ''


@app.route('/remove_top/<email>')
def remove_top_api(email):
    print "remove top called"
    redis.lpop(redis_key_from_email(email))
    return 'remove_top'


@app.route('/list/<email>')
def list_api(email):
    print "list called"
    result = redis.lrange(redis_key_from_email(email), 0, 100)
    json = jsonify(notes=result)
    return json


@app.route('/deltestdata')
def deltestdata_api():
    print 'deleting test data'
    key = redis_key_from_email('test@test.com')
    redis.delete(key)
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
