# coding: utf-8

import base64

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


def redis_book_key_from_email(email):
    return '%s:book' % email


def redis_auth_key_from_email(email):
    return '%s:auth' % email


# TODO: Use brypt lib instead of builtin hash
def hashpw(pw):
    return base64.b64encode(pw)


@app.route('/add', methods=["GET", "POST", "OPTIONS"])
def add_api():
    print "add called"
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        note = json["note"]
        email = json["email"]
        redis.lpush(redis_book_key_from_email(email), note)
        return 'added'

    else:
        print "In non-POST block"
        return ''


@app.route('/remove_top/<email>')
def remove_top_api(email):
    print "remove top called"
    redis.lpop(redis_book_key_from_email(email))
    return 'remove_top'


@app.route('/list/<email>')
def list_api(email):
    print "list called"
    result = redis.lrange(redis_book_key_from_email(email), 0, 100)
    json = jsonify(notes=result)
    return json


@app.route('/deltestdata')
def deltestdata_api():
    print 'deleting test data'
    for email2key in [redis_book_key_from_email,
                      redis_auth_key_from_email]:
        print email2key('test@test.com')
        redis.delete(email2key('test@test.com'))
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/add_user',
           methods=["GET", "POST", "OPTIONS"])
def add_user_api():
    print "add_user called"
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        email = json['email']

        # Account already exists?
        key = redis_auth_key_from_email(email)
        db_pwhash = redis.get(key)
        if db_pwhash:
            return jsonify({'account_created': False}), 200
        else:
            print 'unhashed pw:', json['password']
            user_pwhash = hashpw(json['password'])
            print 'writing hased pw to db:', user_pwhash
            redis.set(key, user_pwhash)
            return jsonify({'account_created': True}), 200
    else:
        print "In non-POST block"
        return ''


@app.route('/authenticate_user',
           methods=["GET", "POST", "OPTIONS"])
def authenticate_user_api():
    print "authenticate_user called"
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        email = json['email']
        password = json["password"]
        print 'userpw', password
        user_hashed_pw = hashpw(password)
        print 'user_hashed_pw,', user_hashed_pw
        db_hashed_pw = redis.get(redis_auth_key_from_email(email))
        print 'dbpw ', db_hashed_pw, type(db_hashed_pw)
        if user_hashed_pw == db_hashed_pw:
            print "successful login"
            return jsonify({'logged_in': True}), 200
        else:
            print "failed login"
            return jsonify({'logged_in': False}), 200
    else:
        print "In non-POST block"
        return ''

# TODO: the POST APIs could share common method
# TODO: remove GET method from all POST apis

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
