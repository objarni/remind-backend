# coding: utf-8

import base64
import uuid

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


#####################
#   redis helpers   #
#####################

# TODO: these are text-only methods. could be moved to separate module.

def redis_book_key_from_email(email):
    return 'book:%s' % email


def redis_auth_key_from_email(email):
    return 'auth:%s' % email


def redis_session_key(ip, token):
    return "session:%s:%s" % (ip, token)


###################
#   P/W hashing   #
###################

# TODO: Use bcrypt lib instead of builtin hash
def hashpw(pw):
    return base64.b64encode(str(hash(pw)))


#####################################
#   Generic POST request handlers   #
#####################################

def open_requesthandler(handler):
    print "Unauthorized API: " + handler.__name__
    if request.method == "POST":
        json = request.get_json()
        return jsonify(handler(json)), 200
    else:
        return ''


def authenticated_requesthandler(handler):
    print "Authorized API: " + handler.__name__
    if request.method == "POST":
        json = request.get_json()
        token = json['token']
        sessionkey = redis_session_key(request.remote_addr, token)
        email = redis.get(sessionkey)
        if email:
            return jsonify(handler(email, json)), 200
        else:
            return jsonify({'status': 'NOSESSION'}), 200
    else:
        return ''


################################
#   Note APIs                  #
################################


@app.route('/add', methods=["OPTIONS", "POST"])
def add_api():

    def add(email, json):
        note = json['note']
        redis.lpush(redis_book_key_from_email(email), note)
        return {'result': 'added'}

    return authenticated_requesthandler(add)


@app.route('/list', methods=["OPTIONS", "POST"])
def list_api():

    def list(email, json):
        result = redis.lrange(redis_book_key_from_email(email), 0, 100)
        return {'notes': result}

    return authenticated_requesthandler(list)


@app.route('/remove_top', methods=["OPTIONS", "POST"])
def remove_top_api():

    def remove_top(email, json):
        redis.lpop(redis_book_key_from_email(email))
        return {'result': 'removed top'}

    return authenticated_requesthandler(remove_top)


#########################
#   Continous testing   #
#########################

@app.route('/deltestdata')
def deltestdata_api():
    print 'deleting test data'
    for email2key in [redis_book_key_from_email,
                      redis_auth_key_from_email]:
        print email2key('test@test.com')
        redis.delete(email2key('test@test.com'))
    return jsonify({'ip': request.remote_addr}), 200


#################################
#   User accounts and sessions  #
#################################

SESSION_EXPIRY_SECONDS = 15


@app.route('/get_email', methods=["OPTIONS", "POST"])
def get_email_api():

    def get_email(email, json):
        return {'email': email}

    return authenticated_requesthandler(get_email)


@app.route('/add_user', methods=["POST", "OPTIONS"])
def add_user_api():

    def add_user(json):
        email = json['email']
        passw = json['password']

        key = redis_auth_key_from_email(email)
        db_pwhash = redis.get(key)

        # Account already exists?
        if db_pwhash:
            return {'account_created': False}
        else:
            user_pwhash = hashpw(passw)
            redis.set(key, user_pwhash)
            return {'account_created': True}

    return open_requesthandler(add_user)


@app.route('/authenticate_user', methods=["POST", "OPTIONS"])
def authenticate_user_api():

    def authenticate_user(json):
        email = json['email']
        password = json["password"]
        user_hashed_pw = hashpw(password)
        db_hashed_pw = redis.get(redis_auth_key_from_email(email))
        if user_hashed_pw == db_hashed_pw:
            print "Successful login, building session."
            token = uuid.uuid1()
            ip = request.remote_addr
            session_key = redis_session_key(ip=ip, token=token)
            redis.set(session_key, email)
            redis.expire(session_key, SESSION_EXPIRY_SECONDS)
            json = {'logged_in': True,
                    'token': token}
            return json
        else:
            print "Failed login"
            return {'logged_in': False}

    return open_requesthandler(authenticate_user)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
