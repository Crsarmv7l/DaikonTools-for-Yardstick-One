#!/usr/bin/python3

from rflib import *
import os
import time

def tx(d, freq, mod, baud, repeat, pre, data, dev=0):
    
    d.setFreq(freq)
    if mod == "ASK":
        d.setMdmModulation(MOD_ASK_OOK)
        
    else:
        d.setMdmModulation(MOD_2FSK)
        d.setMdmDeviatn(dev)
    d.setMdmDRate(baud)
    d.setMaxPower()
    if repeat == 0:
        repeat = 4
    if pre != 0:
        d.RFxmit(pre)
    for x in range (repeat):
        d.RFxmit(data)
        time.sleep(0)
        
    d.setModeIDLE()
    time.sleep(0.5)
    print("Sent")
    

def read(home, a):
    
    os.system('clear')
    
    d = RfCat()
    d.setModeIDLE()
    time.sleep(1)
    
    for i in range(len(a)):
        
        file = open(home + a[i])
        content = file.readlines()
        file.close()
        
        mod=str(content[1]).replace('Mod: ', '')
        mod=mod.strip()
        
        if mod == "ASK":
            freq=str(content[0]).replace('Freq:', '')
            freq=str(freq).replace('.', '')
            freq=int(freq)*10000
	
            baud=str(content[2]).replace('Baud: ', '')
            baud=int(baud)*1
    
            repeat=str(content[3]).replace('Repeat: ', '')
            repeat=repeat.strip()
            repeat=int(repeat)*1

            pre=str(content[4]).replace('Preamble: ', '')
            pre=pre.strip()
            if pre == '':
                pre=0
            else:
                chk=len(pre)
                if (chk % 2) == 0:
                    pre=bytes.fromhex(pre)
                else:
                    print("Preamble hex length is not divisible by 2, cannot convert to bytes")
                    sys.exit(130)

            data=str(content[5]).replace('Data: ', '')
            data=data.strip()
            chk=len(data)
            if (chk % 2) == 0:
                data=bytes.fromhex(data)
            else:
                print("Data hex length is not divisible by 2, cannot convert to bytes")
                sys.exit(130)
                
            print('Sending %s' % a[i])
            tx(d, freq, mod, baud, repeat, pre, data)

        elif mod == "FSK":
            freq=str(content[0]).replace('Freq:', '')
            freq=str(freq).replace('.', '')
            freq=int(freq)*10000
	
            baud=str(content[2]).replace('Baud: ', '')
            baud=int(baud)*1
            
            dev=str(content[3]).replace('Deviation: ', '')
            dev=dev.strip()
            dev=int(dev)*1
    
            repeat=str(content[4]).replace('Repeat: ', '')
            repeat=repeat.strip()
            repeat=int(repeat)*1

            pre=str(content[5]).replace('Preamble: ', '')
            pre=pre.strip()
            if pre == '':
                pre=0
            else:
                chk=len(pre)
                if (chk % 2) == 0:
                    pre=bytes.fromhex(pre)
                else:
                    print("Preamble hex length is not divisible by 2, cannot convert to bytes")
                    sys.exit(130)

            data=str(content[6]).replace('Data: ', '')
            data=data.strip()
            chk=len(data)
            if (chk % 2) == 0:
                data=bytes.fromhex(data)
            else:
                print("Data hex length is not divisible by 2, cannot convert to bytes")
                sys.exit(130)
                
            print('Sending %s' % a[i])
            tx(d, freq, mod, baud, repeat, pre, data, dev)
            
        else:
            print("Unsupported Modulation")
        

def main():
    home = os.path.expanduser( '~/Saved_TX/' )
    
    os.system('clear')
    
    a = []
    
    print(""" 
 /$$$$$$$  /$$                     /$$ /$$             /$$    
| $$__  $$| $$                    | $$|__/            | $$    
| $$  \ $$| $$  /$$$$$$  /$$   /$$| $$ /$$  /$$$$$$$ /$$$$$$  
| $$$$$$$/| $$ |____  $$| $$  | $$| $$| $$ /$$_____/|_  $$_/  
| $$____/ | $$  /$$$$$$$| $$  | $$| $$| $$|  $$$$$$   | $$    
| $$      | $$ /$$__  $$| $$  | $$| $$| $$ \____  $$  | $$ /$$
| $$      | $$|  $$$$$$$|  $$$$$$$| $$| $$ /$$$$$$$/  |  $$$$/
|__/      |__/ \_______/ \____  $$|__/|__/|_______/    \___/  
                         /$$  | $$                            
                        |  $$$$$$/                            
                         \______/                             """)                                                                                                
                                                                                                     
                                                                                                     
    
    print("\nAvailable files:\n")
    for x in os.listdir(home):
        if x.endswith(".ys1"):
            print(x)
 
    path = input("\nEnter filename without extension (* for all): \n")
    if path == '*':
        for x in os.listdir(home):
            if x.endswith(".ys1"):
                a.append(x)
    else:
        path = path + ".ys1"
        a.append(path)
    
        while path != '':
            os.system('clear')
            print("Files not on playlist:\n")
            for x in os.listdir(home):
                if x.endswith(".ys1"):
                    if (x not in a):
                        print(x)
            path = input("\nEnter filename without extension: \n")
            if path != '' and path != "*":
                path = path + ".ys1"
                a.append(path)
    read(home, a)                                        
                    
if __name__ == '__main__':
    main()
