#!/usr/bin/python3

import os
import sys
from rflib import *

#f0f0f0f0f0ff00 works with y
#f0f0f0f0f0fe00 works with z
#OG f0f0ff0
#capture = "f0f0ff33333532b52b4b4d5532b4cb32b280"

def decode(pre, de):
    
    byt=[]
    for i in range(0, len(de), 8):
        byt.append(int(de[i:i+8], 2))

    for n in range(6,0,-1):
        byt[n] = byt[n] ^ byt[n-1]

    for i in range(len(byt)):
        byt[i] = bin(byt[i])[2:].zfill(8)
        
    #print('Pre: ' + pre)
    print('Seed: ' + hex(int(byt[0], 2))[2:])
    print('Control: ' + hex(int(byt[1][0:4], 2))[2:])
    print('Counter: ' + str(int(byt[2]+byt[3], 2)))
    print('Address: ' + hex(int(byt[4] + byt[5] + byt[6], 2))[2:] + "\n")
    
def process(bits):

    de = ""    
    for i in range(0, len(bits), 2):
        if bits[i:i+2] == "01":
            de+= "1"
        if bits[i:i+2] == "10":
            de+= "0"
                    
    return de

def main():
    os.system('clear')
	
    freq = 43342*10000

#setup rfcat
    d = RfCat()
    d.setModeRX()
    d.setFreq(freq)  
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(1600)
    d.setMaxPower()
    d.lowball(1)
	
    print("Press ENTER to stop")
    while not keystop():
		
        try:
            pkt, y = d.RFrecv()
            capture = bin(int.from_bytes(pkt))[2:]
            
            bits = str(capture)
                           
            y = bits.find("1111000011110000111100001111000011110000111111110")
            z = bits.find("1111000011110000111100001111000011110000111111100")
            x = bits.find("1111000011110000111111110")

            if y != -1:
            #retransmission
                pre = "f0f0f0f0f0ff00"
        
                bits = bits[y+49:]
            
                de = process(bits)
                
                if len(de) >= 56:
                    byt = decode(pre, de)
        
            elif z != -1:
            #alt
                pre ="f0f0f0f0f0fe00"
        
                bits = bits[z+49:]
            
                de = process(bits)
               
                if len(de) >= 56:
                    byt = decode(pre, de)

            elif x != -1:
            #first full tx
                pre= "f0f0ff0"
        
                bits = bits[x+25:]

                de = process(bits)
               
                if len(de) >= 56:
                    byt = decode(pre, de)
            else:	
                capture = None

        except ChipconUsbTimeoutException:
            pass 	
    d.setModeIDLE()
    d = None
    


if __name__ == '__main__':
        main()
