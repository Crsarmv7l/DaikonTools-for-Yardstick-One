#!/usr/bin/python3

import os
import sys
import bitstring
from rflib import *

pre ="1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011110000111100001111111"
mid = "000000000000000000000000000000000000000000000000000001111000011110000111100001111000011110000111110000111100001111111"


def manchester(sig):

    de = ""    
    for i in range(len(sig)):
        if sig[i] == "1":
            de+= "01"
        elif sig[i] == "0":
            de+= "10"
            
    return de

def main():
    #Change path
    home = os.path.expanduser( '~/' )

    os.system('clear')

    print("Available files:\n")
    for x in os.listdir(home):
        if x.endswith(".smfy"):
            print(x)
 
    path = input("\nEnter filename without extension: \n")
    
    os.system('clear')
    
    file = open(home + path + ".smfy")
    content = file.readlines()
    file.close()

    freq=int(43342)*10000

    bits = []

    seed = int("A7", 16)
    bits.append(seed)

    p = input("\nEnter the Control (Up, Down, My, Pair): \n")
    if p.lower() == "up":
        control = 2
    elif p.lower() == "down":
        control = 4
    elif p.lower() == "my":
        control = 1
    elif p.lower() == "pair":
        control = 8
    bits.append(control)
    
    press = input("\nEnter press (Long/Short): \n")
    if press.lower() == "long":
        repeat = 7
    elif press.lower() == "short":
        repeat = 1
    

    counter = str(content[2]).replace('Counter: ', '')
    counter = bin(int(counter))[2:].zfill(16)
    c1 = int(counter[0:8], 2)
    bits.append(c1)
    c2 = int(counter[8:16], 2)
    bits.append(c2)

    address = str(content[3]).replace('Address: ', '')
    b4 = int(address[0:2], 16)
    b5 = int(address[2:4], 16)
    b6 = int(address[4:6], 16)

    bits.append(b4)
    bits.append(b5)
    bits.append(b6)

#setup rfcat
    d = RfCat()
    d.setModeRX()
    d.setFreq(freq)  
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(1600)
    d.setMaxPower()
	
    print("Press ENTER to stop")
    while not keystop():
        try:

            scram = bits.copy()
        
            chk = scram[0]
            for i in range(1, len(scram), 1):
                chk = chk^ scram[i]

            chk = chk & 0xf ^ chk >>4
            chk= bin(chk)[2:].zfill(4)

            scram[1] = int((bin(scram[1])[2:] + chk), 2)

            for n in range(1, len(scram), 1):
                scram[n] = scram[n] ^ scram[n-1]
    
            for n in range(len(scram)):
                scram[n] = bin(scram[n])[2:].zfill(8)

            sig = "".join(scram)
    
            rf1 = pre + manchester("0"+ sig) + mid + manchester("0" + sig)
            rf2 = mid + manchester("0" + sig)
        
            bi1 = bitstring.BitArray(bin=rf1).tobytes()
            bi2 = bitstring.BitArray(bin=rf2).tobytes()
           
            d.RFxmit(bi1)
            
            for i in range(repeat):
                d.RFxmit(bi2)
    
            counter = int((bits[2] << 8) | bits[3])
            counter = (counter % 65535) +1
            print("Sending Counter: " + str(counter) + " Command: " + p)

            counter = bin(counter)[2:].zfill(16)
            c1 = int(counter[0:8], 2)
            bits[2] = c1
            c2 = int(counter[8:16], 2)
            bits[3] = c2
		
        except ChipconUsbTimeoutException:
            pass
   
    d.setModeIDLE()
    d = None


if __name__ == '__main__':
        main()
