logis(log is..)
=====

`logis` is Python decorator logger for function, flask view method, result, measuring time. 

### Usage(detail `example.py`)

#### Declare 

```python
import logis
# default is stdout.

logis.addFileLogger() 
# add file log. default path is ./logis.log

logis.setPretty(True) 
# set pretty mode (True|False:default)
```

#### Use in flask 

```python   
@app.route('/')
@logis.flask
def flask():
    return 'Hello World'
```

```
2015-01-07 13:27:03,319	INFO	{
    "date": "2015-01-07 13:27:03.320000", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "127.0.0.1", 
    "type": "WebLog", 
    "url": "/", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
```

#### Use in function

```python  
@app.route('/func')
@logis.flask
def function():
    return str(test(2))

@logis.func
def test(n):
    return n*10
```

```
2015-01-07 13:34:20,631	INFO	{
    "date": "2015-01-07 13:34:20.631000", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "127.0.0.1", 
    "url": "/func", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
2015-01-07 13:34:20,650	INFO	{
    "arguments": {
        "n": 2
    }, 
    "caller": "function", 
    "function": "test", 
    "time": "2015-01-07 13:34:20.650000"
}
```
    
#### Use in function with result
```python  
@app.route('/func')
@logis.flask
def function():
    return str(test(2))

@logis.func
@logis.result
def test(n):
    return n*10
```

```
2015-01-07 13:39:16,263	INFO	{
    "date": "2015-01-07 13:39:16.262000", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "127.0.0.1", 
    "url": "/func", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
2015-01-07 13:39:16,280	INFO	{
    "arguments": {
        "args": [
            2
        ], 
        "kwargs": {}
    }, 
    "caller": "function", 
    "function": "test", 
    "time": "2015-01-07 13:39:16.281000"
}
2015-01-07 13:39:16,282	DEBUG	{
    "function": "test", 
    "result": "20"
}
```

#### Use in function with measuring time 

```python
@app.route('/time')
@logis.flask
@logis.time
def test_time():
    import time
    for i in range(0, 2):
        time.sleep(1)
    return 'Hello World!'
```

```
2015-01-07 13:40:34,009	INFO	{
    "date": "2015-01-07 13:40:34.009000", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "127.0.0.1", 
    "url": "/time", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
2015-01-07 13:40:36,009	DEBUG	{
    "elapsedTime": "0:00:02", 
    "function": "test_time"
}
```

#### If raise exception in @logis.flask or @logis.func, 
```python
@app.route('/error')
@logis.flask
def error():
    raise Exception("test error")
    return 'Hello World!'
```

```
2015-01-07 13:44:09,355	INFO	{
    "date": "2015-01-07 13:44:09.354000", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "127.0.0.1", 
    "url": "/error", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
2015-01-07 13:44:09,355	ERROR	{
    "error": "test error", 
    "time": "2015-01-07 13:44:09.356000", 
    "traceback": "Traceback (most recent call last):...
}
```
#### setPretty 
```python 
logis.setPretty(True) 
```

```
True Case
2015-03-27 15:16:29,395 INFO    {
    "date": "2015-03-27 15:16:29.395482", 
    "method": "GET", 
    "requestData": "", 
    "sourceIp": "121.157.163.130", 
    "url": "/", 
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
}
```

```
False Case
2015-03-27 15:16:29,395 INFO    {"url":"\/login","requestData":"next=http%3A%2F%2Fash84.net%2F","
date":"2015-03-27 15:17:34.050210","userAgent":"Mozilla\/5.0 (Windows NT 6.1; WOW64) 
AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/41.0.2272.101 Safari\/537.36","sourceIp":"121.157.163.130","method":"GET"}
```

### License
MIT License. See `LICENSE.md`