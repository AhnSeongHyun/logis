__author__ = 'sh84.ahn@gmail.com'

from flask import Flask
app = Flask(__name__)

import logis
logis.addFileLogger()


@app.route('/')
@logis.web
def hello_world():
    #test_result(2)
    test_time()
    return 'Hello World!'

@app.route('/index')
@logis.web
@logis.time
def index():
    return 'index'

@logis.result
def test_result(n):
    return n/1


@logis.func
def test_func(n):
    return n/1

@logis.time
def test_time():
    for i in range(0, 100000):
        i+=1


if __name__ == '__main__':
    app.run()


