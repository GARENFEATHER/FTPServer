import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import ThrottledDTPHandler, FTPHandler
from pyftpdlib.servers import FTPServer
from config import *

def init_ftp_server():
	authorizer=DummyAuthorizer()
	if enable_anonymous:
		authorizer.add_anonymous(anonymous_path)
	for user in userList:
		name,pwd,privilege,path=user
		try:
			authorizer.add_user(name, pwd, path, perm=privilege)
		except Exception, e:
			print e
			print user
	dtpHandler=ThrottledDTPHandler
	dtpHandler.read_limit=max_download
	dtpHandler.write_limit=max_upload
	handler=FTPHandler
	handler.authorizer=authorizer
	if enable_logging:
		logging.basicConfig(filename=logging_name, level=logging.INFO)
	handler.masquerade_address=masquerade_address
	handler.passive_ports=range(passive_ports[0], passive_ports[1])
	server=FTPServer((ip, port), handler)
	server.max_cons=max_cons
	server.max_cons_per_ip=max_pre_ip
	server.serve_forever()

def ignoreAnnotation(text):
	for x,content in enumerate(text):
		if content == "#":
			return text[:x]
		pass
	return text

def init_user_connfig():
	f=open("baseftp.ini",'r')
	while True:
		line=f.readline()
		if(len(ignoreAnnotation(line)) > 3):
			userList.append(line.split())
		if not line:
			break
	f.close()

if __name__ == '__main__':
	userList=[]
	init_user_connfig()
	init_ftp_server()

