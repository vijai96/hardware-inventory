import socketio
from gevent import pywsgi
from socketIO_client import SocketIO, LoggingNamespace
from simplecrypt import encrypt,decrypt
import json
import re
import os

flag = 0

socketIO = SocketIO('localhost', 6010, LoggingNamespace)

def on_connect():
    print('connect')

def on_response(args):
	print('alert', args)

def on_alert_1(a):
    if(a[9]=="t"):
        print(a)
        ori = temp
        print('on_alert_1',a)
        socketIO.on('connect', on_connect)
        socketIO.emit('update',{"update":ori})



while(1):
    hwaddr= os.popen('ifconfig -a | grep -Po \'HWaddr \K.*$\' | grep d0').read()
    user= os.popen('whoami').read()
    ram_size= os.popen('sudo dmidecode -t 17 | grep Size').read()
    ram_slots = os.popen('sudo dmidecode -t 16 | grep Number').read()
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
    proc_manu = os.popen('sudo dmidecode -t 4 | grep Manufacturer').read()
    proc_family = os.popen('sudo dmidecode -t 4 | grep Family:').read()

    hw = {"mac":hwaddr,"user": user,"processor":{"manufacturer":proc_manu,"family":proc_family},"ram": {"size": ram_size,"slots":ram_slots},"hdd":{"size": hdd_size},"cpu":{"model":cpu_model,"clock": cpu_clock},"gpu":{"vendor":gpu_vendor,"desc":gpu_desc},"battery":{"name":bat_name,"manufacture_date":bat_manu_date,"serial_no":bat_no},
    "usb": usb}

    var = encrypt('key',user)
    print(var)
    x= decrypt('key',var).decode('ascii')
    #var = var.decode('ascii')
    s = {"enc":x}
    var = json.dumps(s,indent=4,sort_keys=True)


    socketIO.on('connect',on_connect)
    socketIO.emit('encrypt',{"enc":var})





    if(flag==0):
        socketIO.on('connect', on_connect)
        ori = json.dumps(hw,indent=4,sort_keys=True)
        socketIO.emit('original',{"original":ori})
        flag = flag+1
        socketIO.on('alert',on_response)
        socketIO.wait(seconds=1)
        #socketIO.emit('current',{"result":ori})
    else:
        socketIO.on('connect',on_connect)
        temp = json.dumps(hw,indent=4,sort_keys=True)
        time = os.popen('date').read()
        log = {"user":user,"time":time,"lol": "979nouse675758s876876s"}
        log = json.dumps(log,indent=4)
        socketIO.emit('logs',{"log":log})
        if(temp==ori):
            print('no change in the hardware')
        else:
            socketIO.on('connect',on_connect)
            socketIO.emit('alert_neq',{"alert_neq":temp})
            socketIO.on('alert_1',on_alert_1)
            socketIO.wait(seconds=1)
