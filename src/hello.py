import os
from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def hello():
	response = make_response(jsonify(msg='hejsan'))
	response.headers['Access-Control-Allow-Origin'] = "*"
	return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
