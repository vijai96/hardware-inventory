import pymongo
from pymongo import MongoClient
import socketio
from socketIO_client import SocketIO, LoggingNamespace
from gevent import pywsgi
import json
import os
sio = socketio.Server(async_mode='gevent')
con = pymongo.MongoClient('localhost',27017)
o = con.aicte.currentdb
n = con.aicte.newdb
s = con.aicte.scrapdb
@sio.on('connect')
def connect(sid, environ):
    print("connected ", sid)


@sio.on('original')
def original(sid,ori):
    o.save(ori)

@sio.on('alert')
def missing(sid,alert):
    print('device is authenticated')
    c = "true"
    sio.emit('auth_client',c)

@sio.on('update')
def update(sid,update):
    print('updated data in new db')
    s.save(update)



@sio.on('receive')
def message(sid, data):
    x=data
    print(data)
    sio.emit('manage',x)
    c = "true"
    sio.emit('auth_client',c)
    #coll.save(data)




@sio.on('disconnect')
def disconnect(sid):
	print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio)

    # deploy as an eventlet WSGI server
    pywsgi.WSGIServer(('0.0.0.0', 3001), app).serve_forever()
