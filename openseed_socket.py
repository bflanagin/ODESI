#!/usr/bin/python

import sys
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import hive_get as Get
#import hive_submit as Submit
import hive_external_actions as Submit
#import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_connections as Connections
import openseed_chat as Chat
import onetime as OneTime
import openseed_utils as Utils
import openseed_core as Core
import openseed_setup as Settings

settings = Settings.get_settings()

import json

import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		response = ""
		self.data = self.request.recv(131072).strip()

		response = Core.message(self.data)

		self.request.sendall(response.encode("utf8"))

if __name__=="__main__":
	HOST, PORT = "0.0.0.0",8688
	# Create the server, binding to any interface on port 8688
	with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()

	
