#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt  #import the client1
import time

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
from struct import *
import random

mbComPort = 'COM7'   # COM3->RS-485
baudrate = 9600
databit = 8
parity = 'N'
stopbit = 1
mbTimeout = 100 # ms

def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+", result code "+str(rc)+", client_id  "+str(client)
    print(m)

    # first value OFF
    print('set light off!')
    control_light(0)
    client1.publish(topic,0)    

def on_message(client1, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")), message.topic, message.qos, message.retain)
    if message.topic == topic:
        print("set light: ", message.payload)
        if message.payload=='1' or message.payload==1:
            control_light(1)
        else:
            control_light(0)

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def control_light(value):
    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 1
    addr = 2 #base0

    try:
        #-- FC5: write multi-coils
        rr = master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=value)
        print("Write(addr, value)=%s" %(str(rr)))

    except Exception, e:
        print("modbus test Error: " + str(e))

    master._do_close()


def read_power_meter():
    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 4
    #[0x1000-0x1001]=VIn_a
    addr = 0x1000#4096

    v_a = None
    try:
        # FC3
        rr = master.execute(mbId, cst.READ_INPUT_REGISTERS, addr, 4)
        print('read value:', rr)

        # convert to float:
        # IEEE754 ==> (Hi word Hi Bite, Hi word Lo Byte, Lo word Hi Byte, Lo word Lo Byte)
        try:
            v_a_hi = rr[1]
            v_a_lo = rr[0]
            v_a = unpack('>f', pack('>HH', v_a_hi, v_a_lo))
            print('v_a=', v_a)
        except Exception, e:
            print(e)
    except Exception, e:
        print("modbus test Error: " + str(e))

    master._do_close()
    return v_a

# some online free broker:
#   iot.eclipse.org
#   test.mosquitto.org
#   broker.hivemq.com
broker_address="iot.eclipse.org"
topic = "malo-iot/light"
client1 = mqtt.Client()    #create new instance
client1.on_connect = on_connect        #attach function to callback
client1.on_message = on_message        #attach function to callback
#client1.on_log=on_log

time.sleep(1)
client1.connect("iot.eclipse.org", 1883, 60)      #connect to broker
client1.subscribe(topic)

#client1.loop_forever()
# 有自己的while loop，所以call loop_start()，不用loop_forever
client1.loop_start()    #start the loop

while True:
    #v = read_power_meter()
    v = random.randint(100, 120)
    client1.publish("malo-iot/voltage", v)
    time.sleep(2)
