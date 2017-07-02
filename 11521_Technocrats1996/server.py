import pymongo
from pymongo import MongoClient
import socketio
from socketIO_client import SocketIO, LoggingNamespace
from random import randint
from gevent import pywsgi
import json
import os
import logging

con = pymongo.MongoClient('localhost',27017)
c = con.aicte.currentdb
n = con.aicte.newdb
s = con.aicte.scrapdb
e = con.aicte.encdb

sio = socketio.Server(async_mode='gevent')

@sio.on('connect')
def connect(sid, environ):
    print("connected ", sid)

@sio.on('original')
def original(sid,data):
    sio.emit('currentdb',data)
    c.save(data)
    n.save(data)
    print(data)
    #d = "data stored in currentdb"
    #j = {"notice":d }
    #jfinal = json.dumps(x,indent=4,sort_keys=True)
    print("data sent to admin successfully")

@sio.on('original1')
def original(sid,data):
    sio.emit('currentdb1',data)
    c.save(data)
    n.save(data)
    print(data)
    #d = "data stored in currentdb"
    #j = {"notice":d }
    #jfinal = json.dumps(x,indent=4,sort_keys=True)
    print("data sent to admin successfully")

@sio.on('encrypt')
def encrypt(sid,data):
    e.save(data)

@sio.on('windows')
def windows(sid,data):
    sio.emit('currentwindb',data)
    c.save(data)
    n.save(data)
    print(data)
    print("data sent to windows admin successfully")

@sio.on('windows_updated')
def windows_updated(sid,data):
    sio.emit('winup',data)

@sio.on('logs')
def logs(sid,data):
    sio.emit('log',data)


@sio.on('alert_neq')
def alert_neq(sid,data):
    d=data
    ran = randint(0,9)
    if(ran%2==0):
        auth = {"auth":"true"}
        auth = json.dumps(auth,indent=4,sort_keys=True)
    else:
        auth = {"auth":"false"}
        auth = json.dumps(auth,indent=4,sort_keys=True)
    print(auth)
    sio.emit('alert_1',data=auth)

@sio.on('update')
def update(sid,data):
    sio.emit('scrap',data)
    d = data
    print(d)
    s.save(data)
    n.save(data)
    print('data saved in scrapdb')



@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio)

    # deploy as an eventlet WSGI server
    pywsgi.WSGIServer(('0.0.0.0', 6010), app).serve_forever()
