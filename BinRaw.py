#!/usr/bin/python3

from rflib import *
import os
import re
import sys

def tx(freq, mod, baud, data):
	d = RfCat()
	d.setModeIDLE()
	time.sleep(0)
	d.setFreq(freq)
	print('Set Freq: %s' % freq)
	if mod == "ASK":
		d.setMdmModulation(MOD_ASK_OOK)
		print("Set Mod: ASK")
	d.setMdmDRate(baud)
	print('Set Baud: %s' % baud)
	d.setMaxPower()
	
	d.RFxmit(data)
	
	d.setModeIDLE()
	time.sleep(0)
	d = None

def main():

    home = os.path.expanduser( '~/Saved_TX/' )

    os.system('clear')

    print("Available files:\n")
    for x in os.listdir(home):
        if x.endswith(".sub"):
            print(x)
 
    path = input("\nEnter filename: \n")
    
    os.system('clear')
    
    data =""
    with open(home + path + ".sub", 'r') as subfile:
        for line in subfile:
            dataline = re.match(r'^Data_RAW:\s.*', line)
            #print(dataline)
            if dataline:
                values = dataline[0].strip()
                #print(values)
                value = str(values).replace('Data_RAW: ', '').replace(' ', '')
                data+= value
    
    data = bytes.fromhex(data)
    
    file = open(home + path + ".sub", 'r')
    content = file.readlines()
    file.close()
    
    freq = str(content[2]).replace('Frequency: ', '')
    freq = int(freq)
    
    mod = str(content[3]).replace('Preset: ', '')
    if mod == "FuriHalSubGhzPresetOok650Async" or "FuriHalSubGhzPresetOok270Async" :
        mod = "ASK"
    else:
        print("Currently FSK is unsupported")
        sys.exit(130)
    
    test = str(content[4]).replace('Protocol: ', '')
    test = test.strip()
    if test != "BinRAW":
        print("Not BinRaw")
        sys.exit(130)
    
    baud = str(content[6]).replace('TE: ', '')
    baud = 1000000/(int(baud))

    tx(freq, mod, baud, data)
    
    sys.exit(130)
                        

if __name__ == '__main__':
    main()
