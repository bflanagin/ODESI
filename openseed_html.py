#!/usr/bin/python3

import subprocess
import sys
import os
sys.path.append("..")
import json
import time
import openseed_core as Core
import openseed_seedgenerator as Seed
import openseed_account as Account

from bottle import route, run, template, request, static_file

@route('/api', method='POST')
def index():
	themessage = request.forms.get("msg")
	appId = ""
	key = ""
	message = ""
	if len(themessage.split("<::>")) == 3:
		print("Encrypted message")
		appId = themessage.split("<::>")[0]
		key = Account.get_priv_from_pub(appId,"App")
		message = themessage.split("<::>")[1]
		
		decrypted = Seed.simp_decrypt(key,message)
		
		print("From: "+decrypted)
		
		response = Core.message(decrypted)
		encrypt = Seed.simp_crypt(key,response)
		
		print("Returning: "+Seed.simp_decrypt(key,encrypt))
		
		return encrypt
	else:
		print("Non-encrypted message")
		if themessage != None:
			return Core.message(themessage)


run(host='0.0.0.0', port=8670)
