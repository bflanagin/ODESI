#!/usr/bin/python

import sys
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_core as Core
import json
import openseed_seedgenerator as Seed
import openseed_account as Account

import socketserver

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data
    
def chunky(data,sock):
	BUFF_SIZE = 4096 # 4 KiB
	utf8 = data.encode("utf8")
	full_length = len(utf8)
	chunk = 1
	offset = 0
	while True:
		if full_length > BUFF_SIZE:
			#print(utf8[offset:BUFF_SIZE*chunk])
			sock.send(utf8[offset:BUFF_SIZE*chunk])
			full_length -= BUFF_SIZE
		else:
			#print(utf8[offset:full_length])
			sock.send(utf8[offset:full_length])
			break
		
		chunk += 1
		offset += BUFF_SIZE+1
	
	return

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		response = "no response"
		self.data = recvall(self.request).strip()
		
		if self.data.decode().find("msg=") !=-1:
			appId = self.data.decode().split("msg=")[1].split("<::>")[0]
			key = Account.get_priv_from_pub(appId,"App")
			message = self.data.decode().split("msg=")[1].split("<::>")[1]
			if len(self.data.decode().split("msg=")[1].split("<::>")) == 3:
				decrypted = Seed.simp_decrypt(key,message)
				#print("From: "+decrypted)
				#response = Core.message(message)
				response = Core.message(decrypted)
				#print("Returning: "+response)
				encrypt = Seed.simp_crypt(key,response)
				#json.loads(Seed.simp_decrypt(key,encrypt))
				#encrypt = response
				#print("Returning: "+Seed.simp_decrypt(key,encrypt))
				chunky(encrypt.strip(),self.request)
				#self.request.sendall(response.encode("utf8"))
			else:
				print('{"server":"error incomplete message"}')
				print(self.data)
				self.request.send(str('{"server":"error incomplete message"}').encode("utf8"))
		else:
			response = Core.message(self.data)
			try:
				json.loads(response)
			except:
				print("not json formated on return of",self.data)
			else:
				chunky(response.strip(),self.request)

if __name__=="__main__":
	HOST, PORT = "0.0.0.0",8688
	# Create the server, binding to any interface on port 8688
	with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()

	
