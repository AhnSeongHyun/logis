__author__ = 'sh84.ahn@gmail.com'

from flask import Flask
app = Flask(__name__)

import logis
logis.addFileLogger()

@app.route('/')
@logis.flask
def flask():
    return 'Hello World!'

@app.route('/func')
@logis.flask
def function():
    return str(test(2))

@logis.func
@logis.result
def test(n):
    return n *10

@logis.func
@logis.result
def test_with_result(n):
    return n *10


@app.route('/result')
@logis.flask
@logis.result
def flask_with_result():
    return 'Hello World!'


@app.route('/time')
@logis.flask
@logis.time
def test_time():
    import time
    for i in range(0, 2):
        time.sleep(1)
    return 'Hello World!'


@app.route('/error')
@logis.flask
def error():
    raise Exception("test error")
    return 'Hello World!'



if __name__ == '__main__':
    app.run()




