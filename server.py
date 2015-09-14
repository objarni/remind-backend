# coding: utf-8
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.debug = True

notes = []


def tmpresponse(o):
    response = make_response(o)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route('/add')
def add_api():
    notes.append("test count=" + str(len(notes)))
    return tmpresponse('added')


@app.route('/remove_top')
def remove_top_api():
    notes.pop()
    return tmpresponse('remove_top')


@app.route('/list')
def list_api():
    reversed = list(notes)
    reversed.reverse()
    json = jsonify(notes=reversed)
    return tmpresponse(json)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
