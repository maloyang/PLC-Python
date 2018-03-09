#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time

mbComPort = 'COM7'   # your RS-485 port. for linux --> "/dev/ttyUSB2"
baudrate = 9600
databit = 8 #7, 8
parity = 'N' #N, O, E
stopbit = 1 #1, 2
mbTimeout = 100 # ms
ser = None
sendBuf = None


def main():

    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 1
    #addr = 0 #base0
    addr = 2 #base0 --> my 110V Led燈泡

    for i in range(5):
        try:
            value = i%2
            #-- FC5: write multi-coils
            rr = master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=value)
            print("Write(addr, value)=%s" %(str(rr)))

        except Exception, e:
            print("modbus test Error: " + str(e))

        time.sleep(2)

    master._do_close()


if __name__ == '__main__':
    main()

