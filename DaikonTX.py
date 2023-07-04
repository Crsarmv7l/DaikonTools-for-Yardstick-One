#!/usr/bin/python3
from rflib import *
import os
import time
import sys

def ask(mod, home, path):
	file = open(home + path + ".ys1")
	content = file.readlines()
	file.close()

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
		
	tx(freq, mod, baud, repeat, pre, data)

def fsk(mod, home, path):
	file = open(home + path + ".ys1")
	content = file.readlines()
	file.close()

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
			print("Pre hex length is not divisible by 2, cannot convert to bytes")
			sys.exit(130)

	data=str(content[6]).replace('Data: ', '')
	data=data.strip()
	chk=len(data)
	if (chk % 2) == 0:
		data=bytes.fromhex(data)
	else:
		print("Data hex length is not divisible by 2, cannot convert to bytes")
		sys.exit(130)
	tx (freq, mod, baud, repeat, pre, data, dev)

def tx(freq, mod, baud, repeat, pre, data, dev=0)
	d = RfCat()
	d.setModeIDLE()
	time.sleep(1)
	d.setFreq(freq)
	print('Set Freq: %s' % freq)
	if mod == "ASK":
		d.setMdmModulation(Mod_ASK_OOK)
		print("Set Mod: ASK")
	else:
		d.setMdmModulation(MOD_2FSK)
		print("Set Mod: FSK")
		d.setMdmDeviatn(dev)
		print('Set Deviation: %s' % dev)
	d.setMdmDRate(baud)
	print('Set Baud: %s' % baud)
	d.setMaxPower()
	#d.setAmpMode(ampmode=1)
	if repeat == 0:
		print("Continuous playback, press ENTER to Stop")
		if pre == 0:
			print("No Preamble")
		else:
			d.RFxmit(pre)
		while not keystop():
			try:
				d.RFxmit(data)
			except ChipconUsbTimeoutException:
				pass
	else:
		print('Total Repeats:%s' % repeat)
		if pre == 0:
			print("No Preamble")
		else:
			d.RFxmit(pre)
		for x in range (repeat):
			d.RFxmit(data)
			time.sleep(0)
	d.setModeIDLE()
	time.sleep(1)
	d = None
	sys.exit(130)
	
def main():

	home = os.path.expanduser( '~/Saved_TX/' )

	os.system('clear')

	print("Available files:\n")
	for x in os.listdir(home):
		if x.endswith(".ys1"):
			print(x)
 
	path = input("\nEnter filename without extension: \n")
    
	os.system('clear')

	file = open(home + path + ".ys1")
	content = file.readlines()
	file.close()

	mod=str(content[1]).replace('Mod: ', '')
	mod=mod.strip()

	if mod == "ASK":
		ask(mod, home, path)
	elif mod == "FSK":
		fsk(mod, home, path)
	else:
		print("Unsupported Modulation")


if __name__ == '__main__':
    main()
