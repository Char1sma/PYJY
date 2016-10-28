# -*- coding: utf-8 -*-
#
# FileName		: whois.py
# Description		: whois domain
# Version		: 0.1 alpha 1
# Date			: 2016-10-28
#
import sys,socket
def query(url):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('whois.networksolutions.com',43))
	s.send((url+' \r\n').encode('utf-8'))
	while True:
		v = s.recv(1024)
		if v=='' or v == None:
			break
		print (v.decode('utf8'))
	s.close()

def argv_im(argvs):
	count = len (argvs)
	if count == 1:
		print('Usage: whois.py domain')
	elif count == 2:
		query (argvs[1])
	else:
		print("Unknown Option:",argvs[1:count])

argv_im(sys.argv)