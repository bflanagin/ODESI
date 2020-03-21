#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
import json
import subprocess
sys.path.append("..")
import openseed_seedgenerator as Seed
from steem import Steem
thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
s = Steem(nodes=thenodes)

import openseed_setup as Settings

settings = Settings.get_settings()


class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		response = ""
		self.data = self.request.recv(131072).strip()
		from_client = json.loads(self.data)

# Gather nodes by checking their status. Each server is responsible for its children. If the Progentor can not be found First priority takes over.
	def gather_servers(seed):

		return

# Used for decreasing sync load. only data required for apps known to the server is synced. 
	def gather_apps():
		openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
		apps = []
		gather = "SELECT * FROM `applications` WHERE 1"
		
		return


#server level userdabase that stores only tokens. Refreshed daily. Used to decrease sync load. If user isn't on the server no data is synced for the user.
	def gather_users():

		return


# Initiate connection and request new data in the order of priority

	def start_round():


		return
	
class Round:
	
	# Sends current hash of database to fellow server
	
	def send_hash(dbname):
		thehash = ""
		return thehash

	# Check database hash against another

	def check_hash(dbname,thehash):
		thehash = ""
		return thehash
	
	# create priority list (returned as an array) to begin transfer round.

	def get_priority():
		priority = []

		return priority

	# If the database hash comes back different ask for changes since last time stamp

	def request_changes(dbname,last_timestamp):
		
		return

	# The more outgoing brother of request changes, send changes sends the changes.  

	def send_changes(dbname,last_timestamp):

		return

	# Beyond using the applications to dictate what data to store it would behoove the servers to remember "remote" users that are in the chat rooms that users are a part of. 
	# If this works as expected then users should "drop off" or never store on servers that know nothing about either user.

	def chat_com():

		

		return
		
	

class Servers:
	
	# We register the servers that "call home" and check them against known servers. If they don't exist in the database we add them to the lowest priority by default. 
 
	def register_server(ipaddress,seed):

	return

	# Check if server can send and recieve. If server is behind firewalls they're priority will always be greater than 1.

	def check_io(ipaddress,seed):

	return

	def check_send(seed):

	return


	def check_recieve(seed):

	return

	# Update priority based on pscore. This includes IO, uptime, transferspeeds, distance

	def update_priorities(seed):
		newpriority = ""
		return newpriority




if __name__=="__main__":
	HOST, PORT = "0.0.0.0",8689
	# Create the server, binding to any interface on port 8688
	with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()
	
