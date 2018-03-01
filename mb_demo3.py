#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
from struct import *

mbComPort = 'COM6'   # COM3->RS-485
baudrate = baudrate = 19200
databit = 8
parity = 'N'
stopbit = 1
mbTimeout = 100 # ms
ser = None
sendBuf = None


def main():

    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 4
    #[0x1000-0x1001]=VIn_a
    addr = 0x1000#4097

    try:
        # FC3
        rr = master.execute(mbId, cst.READ_INPUT_REGISTERS, addr, 10)
        print('read value:', rr)

        # convert to float:
        #IEEE754 ==> (Hi word Hi Bite, Hi word Lo Byte, Lo word Hi Byte, Lo word Lo Byte)
        try:
            v_a_hi = rr[1]
            v_a_lo = rr[0]
            v_a = unpack('>f', pack('>HH', v_a_hi, v_a_lo))
            print('v_a=', v_a)
            #struct.unpack(">f",'\x42\xd8\x6b\x8d')
        except Exception, e:
            print(e)

    except Exception, e:
        print("modbus test Error: " + str(e))
        return


    master._do_close()


if __name__ == '__main__':
    main()

