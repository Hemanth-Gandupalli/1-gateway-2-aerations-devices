import time
from datetime import datetime,timedelta
import json
import os, sys
import struct
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
print("\n-- LoRa Gateway --\n")
recv_slot=[[1,5],[6,11],[12,17],[18,23],[24,29],[30,35],[36,41],[42,47],[48,53],[54,59]]
sleep = [[5,6],[11,12],[17,18],[23,24],[29,30],[35,36],[41,42],[47,48],[53,54],[59,0]]
if __name__ == "__main__":
    while True:
        for i, slot in enumerate(recv_slot):
                current_min = datetime.now().minute
                if slot[0] <= current_min < slot[1]:
                    print("-------------Gateway shifts to reciving mode---------------")
                    LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING, LoRa.RX_GAIN_AUTO)
                    LoRa.request()
                    LoRa.wait(1)
                    try:
                        rcv_data=[]
                        while LoRa.available():
                            rcv_data.append(LoRa.read())
                        print(rcv_data)
                        rcv_data = bytes(rcv_data)
                        unstruct_data = struct.unpack('7f',rcv_data)
                        # print("Recieved data--->",unstruct_data)
                        sensor1 = unstruct_data[0]
                        sensor2 = unstruct_data[1]
                        sensor3 = unstruct_data[2]
                        sensor4 = unstruct_data[3]
                        x = unstruct_data[4]
                        y = unstruct_data[5]
                        z = unstruct_data[6]
                        with open("data.json",'r') as f:
                            data = json.load(f)
                        data["sensor1"] = sensor1
                        data["sensor2"] = sensor2
                        data["sensor3"] = sensor3
                        data["sensor4"] = sensor4
                        data["x"] = x
                        data["y"] = y
                        data["z"] = z
                        with open("data.json",'w') as f:
                            json.dump(data,f)
                        with open ('status.txt','r') as file:
                            s = file.read()
                        if s == "True":
                            print("Recieved data--->",unstruct_data)
                        else:
                            print("Recieved data---> 0,0,0,0,0,0,0")
                            
                    except Exception as e:
                        print(e)
                    status = LoRa.status()
                    if status == LoRa.STATUS_CRC_ERR : print("CRC error")
                    elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
                    time.sleep(4)  
            
            

        
        
    
