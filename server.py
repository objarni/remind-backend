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


#####################
#   redis helpers   #
#####################


def redis_book_key_from_email(email):
    return '%s:book' % email


def redis_auth_key_from_email(email):
    return '%s:auth' % email


###################
#   P/W hashing   #
###################

# TODO: Use bcrypt lib instead of builtin hash
def hashpw(pw):
    return base64.b64encode(str(hash(pw)))


##################################
#   Post request common method   #
##################################

def handle_postrequest(handle_json):
    print handle_json.__name__
    print "method=" + repr(request.method)
    if request.method == "POST":
        print "In POST block"
        json = request.get_json()
        return handle_json(json)
    else:
        print "In non-POST block"
        return ''


################################
#   list/remove_top/add APIs   #
################################


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


@app.route('/add_user', methods=["POST", "OPTIONS"])
def add_user_api():

    def add_user(json):
        email = json['email']
        key = redis_auth_key_from_email(email)
        db_pwhash = redis.get(key)
        # Account already exists?
        if db_pwhash:
            return jsonify({'account_created': False}), 200
        else:
            user_pwhash = hashpw(json['password'])
            redis.set(key, user_pwhash)
            return jsonify({'account_created': True}), 200

    return handle_postrequest(add_user)


@app.route('/authenticate_user', methods=["POST", "OPTIONS"])
def authenticate_user_api():

    def authenticate_user(json):
        email = json['email']
        password = json["password"]
        user_hashed_pw = hashpw(password)
        db_hashed_pw = redis.get(redis_auth_key_from_email(email))
        if user_hashed_pw == db_hashed_pw:
            print "successful login"
            return jsonify({'logged_in': True}), 200
        else:
            print "failed login"
            return jsonify({'logged_in': False}), 200

    return handle_postrequest(authenticate_user)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
