# coding: utf-8
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.debug = True


@app.route('/list')
def hello():
    notes = [
        'Brannbara CD nästan slut',
        'Blogga om bla bla bla',
        'Glöm inte betala danskursen faktura i mail',
    ]
    json = jsonify(msg='hejsan',
                   notes=notes)
    response = make_response(json)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
