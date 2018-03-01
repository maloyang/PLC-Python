#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time

mbComPort = 'COM6'   # COM3->RS-485
baudrate = 9600
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

    mbId = 1
    addr = 1000 #base0
    #addr = 2 #base0

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


    # read demo
    '''
    #-- DI read: FC2  Read multi-input discrete ( 1xxxx )
    rr = master.execute(mbId, cst.READ_DISCRETE_INPUTS, self.diAddress[idx], self.diN[idx])
    for i in range(self.diN[idx]):
        self.di[idx][i] = rr[i]
    self.logDebug("[%d] DI value= %s" %(idx, rr))

    #-- FC01: Read multi-coils status (0xxxx) for DO
    rr = master.execute(mbId, cst.READ_COILS, self.doAddress[idx], self.doN[idx])
    for i in range(self.doN[idx]):
        self.do[idx][i] = rr[i]
    self.logDebug("[%d] DO value= %s" %(idx, rr))

    #-- FC04: read multi-input registers (3xxxx), for AI
    rr = master.execute(mbId, cst.READ_INPUT_REGISTERS, self.aiAddress[idx], self.aiN[idx])
    for i in range(self.aiN[idx]):
        self.ai[idx][i] = rr[i]
    self.logDebug("[%d] AI value= %s" %(idx, rr))

    #-- FC03: read multi-registers (4xxxx) for AO
    rr = master.execute(mbId, cst.READ_HOLDING_REGISTERS, self.aoAddress[idx], self.aoN[idx])
    for i in range(self.aoN[idx]):
        self.ao[idx][i] = rr[i]
    self.logDebug("[%d] AO value= %s" %(idx, rr))

    # FC3
    rr = master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, 1)
    print('rr:', rr)
    '''