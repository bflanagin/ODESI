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

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		response = ""
		self.data = self.request.recv(131072).strip()
		if self.data.find("msg=") !=-1:
			appId = self.data.split("msg=")[1].split("::")[0]
			key = Accout.get_priv_from_pub(appId)
			response = Core.message(Seed.simp_decrypt(key,self.data.split("msg=")[1].split("::")[1]))
			self.request.sendall(response.encode("utf8"))

if __name__=="__main__":
	HOST, PORT = "0.0.0.0",8688
	# Create the server, binding to any interface on port 8688
	with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()

	
