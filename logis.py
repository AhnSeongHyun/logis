__author__ = 'sh84.ahn@gmail.com'
__version__ = '0.1'

import logging
from logging import handlers
import inspect
import functools
import datetime
import json
import os
from flask import request

""" LogLevel """


@property
def CRITICAL():
    return logging.CRITICAL

@property
def FATAL():
    return logging.FATAL

@property
def ERROR():
    return logging.ERROR

@property
def WARNING():
    return logging.WARNING
@property
def INFO():
    return logging.INFO

@property
def DEBUG():
    return logging.DEBUG

@property
def NOTSET():
    return logging.NOTSET

log_format ='%(asctime)s\t%(levelname)s\t%(message)s'

logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger('logis')
logger.setLevel(logging.DEBUG)

def addFileLogger(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)) , "logis.log")):
    file_handler = handlers.TimedRotatingFileHandler(filename=filename, when='D', interval=1)
    file_handler.formatter = logging.Formatter(log_format)
    logging.getLogger('logis').handlers.append(file_handler)

def setLevel(level):
    logger.setLevel(level)

""" LogClass """

class BasicLog():
    """
    Goal : class to json
    """
    def __init__(self):
        pass

    def toJson(self):
        return json.dumps(vars(self), sort_keys=True, indent=4)
 

class WebLog(BasicLog):
    sourceIp = None
    url = None
    requestData = None
    method = None
    userAgent = None
    date = None

    def __init__(self, sourceIp=None, url=None, requestData=None, method=None, userAgent=None, date=None):
        BasicLog.__init__(self)
        self.sourceIp = sourceIp
        self.url = url
        self.requestData = requestData
        self.method = method
        self.userAgent = userAgent
        self.date = str(date) 

class LogicLog(BasicLog):
    function = None
    caller = None
    arguments = None
    time = None

    def __init__(self, function=None, caller=None, arguments=None, time=None):
        BasicLog.__init__(self)
        self.function = function
        self.caller = caller
        self.arguments = arguments
        self.time = str(time)


class ResultLog(BasicLog):
    function = None
    result = None

    def __init__(self, function=None, result=None):
        BasicLog.__init__(self)
        self.function = function
        self.result = str(result)

class ElapsedTimeLog(BasicLog):
    function = None
    elapsedTime = None

    def __init__(self, function=None, elapsedTime=None):
        BasicLog.__init__(self)
        self.function = function
        self.elapsedTime = str(elapsedTime)


class ErrorLog(BasicLog):
    time = None
    error = None
    traceback = None

    def __init__(self, time=None, error=None, traceback=None):
        BasicLog.__init__(self)
        self.time = str(time)
        self.error = error
        self.traceback = traceback

""" Decorator """


def result(func):
    """
    Goal : log for result
    Running Location : After function
    """
    @functools.wraps(func)
    def newFunc(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(ResultLog(function = func.__name__, result=result).toJson())

        return result
    return newFunc


def time(func):
    """
    Goal : Measure time
    Running Location : After function
    """
    @functools.wraps(func)
    def newFunc(*args, **kwargs):
        st = datetime.datetime.now()
        result = func(*args, **kwargs)
        ed = datetime.datetime.now()
        elapsed = ed-st
        logger.debug(ElapsedTimeLog(function = func.__name__, elapsedTime=elapsed).toJson())
        return result
    return newFunc


def flask(func):
    @functools.wraps(func)
    def newFunc(*args, **kwargs):
        result = None
        error = None
        tb = None

        m = request.method
        requestData = None
        if(m=='GET'):
            requestData = request.query_string
        else:
            requestData = request.form

        from urlparse import urlparse

        logger.info(
        WebLog(sourceIp=request.remote_addr,
                    url=urlparse(request.url).path,
                    requestData=requestData,
                    method=m,
                    userAgent=str(request.user_agent),
                    date=datetime.datetime.now()).toJson())

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            import traceback
            error = e.message
            tb =  traceback.format_exc()
            logger.error(ErrorLog(time=datetime.datetime.now(),
                                  error=error,
                                  traceback=tb).toJson())
        return result
    return newFunc

 

def func(func):
    """
    Goal : General Function Log
    Running Location : Before function
    """
    @functools.wraps(func)
    def newFunc(*args, **kwargs):
        arguments = inspect.getcallargs(func, *args, **kwargs)

        logger.info(LogicLog(function = func.__name__,
                             caller =  inspect.stack()[1][3],
                             arguments = arguments,
                             time =  datetime.datetime.now()).toJson())
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            import traceback
            error = e.message
            tb = traceback.format_exc()
            logger.error(ErrorLog(time=datetime.datetime.now(),
                                  error=error,
                                  traceback=tb).toJson())
        return result
    return newFunc