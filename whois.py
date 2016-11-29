# -*- coding: utf-8 -*-
#
# FileName		: whois.py
# Description		: whois domain
# Version		: 0.1 alpha 2
# Date			: 2016-10-28
# Update		: 2016-11-29
#
import sys,socket
def query(server, port, parameter) :
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((server,port))
	sock.send(parameter.encode('utf-8'))
	msg = ''
	count = 0
	while True:
		chunk = sock.recv(1000).decode('utf-8')
		if (len(chunk) == 0):
			count = count + 1
			if count > 5:
				break
		else:
			count = 0
		msg = msg + chunk
	return msg
	
def get_whois_server(domain) :
	whois_servers = {'com':'whois.verisign-grs.com','net':'whois.verisign-grs.com','org':'whois.pir.org','edu':'whois.educause.edu','name':'whois.nic.name','info':'whois.afilias.net'}
	domain = domain.replace('http://','')
	domain = domain.replace('www.','')
	if domain.rfind('/') > 0:
		domain = domain[0:domain.rfind('/')]
	return whois_servers[domain[domain.rfind('.')+1:]]

def argv_im(argvs) :
	count = len (argvs)
	if count == 1:
		print('Usage: whois.py domain')
	elif count == 2:
		para =  argvs[1] + "\r\n"
		print (query(get_whois_server(argvs[1]),43,para))
	else:
		print("Unknown Option:",argvs[1:count])

argv_im(sys.argv)