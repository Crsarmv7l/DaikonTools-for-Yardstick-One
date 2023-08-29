#!/usr/bin/python3

from rflib import *
import time
from sys import exit
import os

t = time.localtime()
curr=time.strftime("%H:%M", t)

def lacrosse(st):
	st = st.strip().split('0')
	p=""
	for b in st:
		if b == "1111" or b =="111":
			p+="0"
		elif b == "1" or b == "11":
			p+= "1"
	if len(p) == 44:
		t1 = str(int(p[20:24], 2))
		t2 = str(int(p[24:28], 2))
		t3 = str(int(p[28:32], 2))
		temp= str(int(t1+t2) - 50)+ "." + t3
		temp = round((((int(temp)/10)*(9/5)) + 32), 1)
		print("\nLacrosse:")
		print('Temp: %s C' % temp)
		print('Updated: %s' % curr)

def infactory(cap):
	cap = cap.replace('11', '1')
	bits = cap.strip().split('1')
	st=''
	for b in bits:
		if b == "00000" or b == "000000":
			st+= "0"
		elif b == "00000000000" or b == "000000000000":
			st+="1"
		else:
			st+=" "
	f= st.strip().split(" ")
	
	flag=0
	for b in f:
		if len(b) == 40 and flag == 0:
			flag = flag + 1
			temp = round(((int(b[16:28], 2)/10) - 90), 1)
			hum1 = str(int(b[28:32], 2))
			hum2 = str(int(b[32:36], 2))
			hum = hum1+hum2
			print("\ninFactory:")
			print('Temp: %s F' % temp)
			print('Humidity: %s' % hum)
			print('Updated: %s' % curr)

def decode(p):
	x=p[12:24]
	y=p[28:]
	temp = round((((int(x, 2))/10)*(9/5) +32), 1)
	hum = int(y, 2)
	print("\nNexus:")
	print('Temp: %s F' % temp)
	print('Humidity: %s' % hum)
	print('Updated: %s' % curr)
	del(p)

def sort(bit):
	pwmbits=""
	for i in range(len(bit)):
		if bit[i] == "000" or bit[i] == "00":
			pwmbits+="0"
		elif len(bit[i]) > 8:
			pwmbits+="x"
		elif bit[i] != '' and bit[i] != "0":
			pwmbits+="1"

	p=pwmbits.strip().split('x')
	del bit
	
	flag=0
	for i in range(len(p)):
		if len(p[i]) == 36 and flag == 0:
			flag = flag + 1
			decode(p[i])
	del pwmbits
	del p	

def main():
	os.system('clear')
	
	freq = int(43392*10000)

#setup rfcat
	d = RfCat()
	d.setModeRX()
	d.setFreq(freq)  
	d.setMdmModulation(MOD_ASK_OOK)
	d.setMdmDRate(2900)
	d.setMaxPower()
	d.lowball(1)
	
	print("Press ENTER to stop")
	while not keystop():
		
		try:
			pkt, y = d.RFrecv()
			capture = bin(int.from_bytes(pkt))[2:]
			cap = str(capture)
			x = cap.find('1000000100000010000001000000')
			if x != -1:
				if len(cap) > 36:
						bit=cap[x:].strip().split('1')
						sort(bit)
			y = cap.find('111000111000111000')
			if y != -1:
				y =	cap.find('100000000000000000000000')
				if y != -1:
					infactory(cap[y:])
			z = cap.find('0000111100011110001111000111100011')
			if z != -1:
				st = cap[z:]
				a = st.find('00000')
				if a != -1:
				#Only 2 repeats with Lacrosse. trying to catch either two chances to decode each tx
					lacrosse(st[:a])

					lacrosse(st[a:])

			else:	
				del capture	
		except ChipconUsbTimeoutException:
			pass 	
	d.setModeIDLE()
	d = None

if __name__ == '__main__':
    main()
    sys.exit(0)
