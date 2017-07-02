import socketio
from gevent import pywsgi
from socketIO_client import SocketIO, LoggingNamespace
import json
import re
import os
sio = socketio.Server(async_mode='gevent')
soc = SocketIO('localhost', 6010, LoggingNamespace)

def on_connect():
    print('connect')

def auth_client(auth):
    print('auth')
    if(auth=="true"):
        ori=X
        print('yyyyyyyy')
        soc.emit('update',{"update":ori})


run=1


hwaddr= os.popen('ifconfig -a | grep -Po \'HWaddr \K.*$\' | grep d0').read()
user= os.popen('whoami').read()
ram_size= os.popen('sudo dmidecode -t 17 | grep Size').read()
hdd_size= os.popen('sudo hdparm -I /dev/sda | grep device | grep size').read()
cpu_model= os.popen('sudo lscpu | grep Model | grep name').read()
cpu_clock= os.popen('sudo lscpu | grep CPU | grep MHz').read()
gpu_vendor= os.popen('sudo lshw -class display | grep vendor').read()
gpu_clock= os.popen('sudo lshw -class display | grep clocksudo lshw -class displau | grep description').read()
gpu_desc= os.popen('sudo lshw -class displau | grep description').read()
bat_manu_date= os.popen('sudo dmidecode -t 22 | grep Manufacture | grep Date').read()
bat_no= os.popen('sudo dmidecode -t 22 | grep Serial | grep Number').read()
bat_name= os.popen('sudo dmidecode -t 22 | grep Name').read()
usb= os.popen('sudo lsusb').read()

hw = {"mac":hwaddr,"user": user,"ram": {"size": ram_size},"hdd":{"size": hdd_size},"cpu":{"model":cpu_model,"clock": cpu_clock},"gpu":{"vendor":gpu_vendor,"desc":gpu_desc},"battery":{"name":bat_name,"manufacture_date":bat_manu_date,"serial_no":bat_no},
"usb": usb}

if(run==0):
    ori=json.dumps(hw,indent=4,sort_keys=True)
    #soc.on('connect', on_connect)
    soc.emit('original',{"original": ori})
    run = run+1
else:
    ori= "haha"
    x = json.dumps(hw,indent=4,sort_keys=True)
    soc.emit('receive',{"result":x})
    if(x==ori):
        print('ignored u idiot')
    else:
            #soc.on('connect', on_connect)
            soc.emit('alert', {'alert':x})
            soc.on('auth_client',auth_client)











'''
@sio.on('disconnect')
def disconnect(sid):
	print('disconnect ', sid)
'''
