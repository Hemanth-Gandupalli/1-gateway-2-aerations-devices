import time
from datetime import datetime,timedelta
import json
import os, sys
import struct
from random import uniform


currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time
from gpiozero import CPUTemperature
busId = 0; csId = 0
resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
LoRa = SX127x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

print("Set frequency to 433 Mhz")
LoRa.setFrequency(433000000)


print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
LoRa.setSpreadingFactor(7)
LoRa.setBandwidth(125000)
LoRa.setCodeRate(4/5)

print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)
LoRa.setPreambleLength(12)
LoRa.setPayloadLength(15)
LoRa.setCrcEnable(True)

print("Set syncronize word to 0x34")
LoRa.setSyncWord(0x34)
print("\n-- LoRa Node1 --\n")
send_slot=[[1,5],[12,17],[24,29],[36,41],[48,53]]
sleep = [[5,12],[17,24],[29,36],[41,48],[53,0]]
while True:
    for i, slot in enumerate(send_slot):
            current_min = datetime.now().minute
            if slot[0] <= current_min < slot[1]:
                print("-------------Gateway shifts to sending mode---------------")
                sensor1 = uniform(2.20, 2.48)
                sensor2 = uniform(1.08, 1.5)
                sensor3 = uniform(3.30, 3.59)
                sensor4 = uniform(4.25, 4.66)
                x = uniform(5.5, 5.9)
                y = uniform(6.0, 6.4)
                z = uniform(7.13, 7.48)
                datalist = [sensor1,sensor2,sensor3,sensor4,x,y,z]
                struct_data = struct.pack('7f',datalist[0],datalist[1],datalist[2],datalist[3],datalist[4],datalist[5],datalist[6])
                print("bytes_data ",struct_data)
                message = list(struct_data)
                print("struct_data --> ",message)
                LoRa.setTxPower(17, LoRa.TX_POWER_PA_BOOST)
                LoRa.beginPacket()
                LoRa.write(message,len(message))
                LoRa.endPacket()
                LoRa.wait()
                print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))
                time.sleep(5)