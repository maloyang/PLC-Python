#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu


mbComPort = 'COM7'
baudrate = 38400
databit = 8
parity = 'N'
stopbit = 1
mbTimeout = 100 # ms

def main():

    # scan_test:
    for baudrate in [9600, 19200, 38400, 115200]:
        for parity in ['N', 'O', 'E']:
            for stopbit in[1, 2]:
                print('scan @', baudrate, parity, stopbit)
                mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
                master = modbus_rtu.RtuMaster(mb_port)
                master.set_timeout(mbTimeout/1000.0)

                mbId = 1
                addr = 0xFA
                ao_n = 1

                try:
                    # FC3
                    rr = master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, 1)
                    print('rr:', rr)

                except Exception, e:
                    print("modbus test Error: " + str(e))

                master._do_close()


if __name__ == '__main__':
    main()
