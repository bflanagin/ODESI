#!/usr/bin/python
import cgi
import cgitb
import sys
import urllib
sys.path.append("..")

import openseed_account as Account
import openseed_setup as Settings
import openseed_seedgenerator as Seeds
import openseed_music as Music
import openseed_connections as Connections
import openseed_chat as Chat
import onetime as OneTime

import json
form = cgi.FieldStorage()

dev_pub = form.getvalue("pub")
read_json = form.getvalue("msg")

print("Content-type:text/html\r\n\r\n")

if dev_pub == None:
	from_client = json.loads(read_json)
else:
	devID = Account.get_priv_from_pub(dev_pub)
	decrypted_message = Seeds.simp_decrypt(devID,read_json)
	from_client = json.loads(decrypted_message)

action = from_client["act"]

if Account.check_appID(from_client["appID"],from_client["devID"]):
	app = from_client["appID"]
	dev = from_client["devID"]
	
	print("We're Here")


