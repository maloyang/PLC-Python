#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time

mbComPort = 'COM7'
baudrate = 9600
databit = 8
parity = 'N'
stopbit = 1
mbTimeout = 100 # ms

def main():

    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 1
    addr = 1000 #base0

    for i in range(5):
        try:
            # FATEK的PLC把DI點放在DO的address中
            #-- FC01: Read multi-coils status (0xxxx) for DO
            rr = master.execute(mbId, cst.READ_COILS, addr, 4)
            print("value= ",  rr)

        except Exception, e:
            print("modbus test Error: " + str(e))

        time.sleep(1)

    master._do_close()


if __name__ == '__main__':
    main()

