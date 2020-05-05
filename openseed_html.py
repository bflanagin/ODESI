#!/usr/bin/python3

import subprocess
import sys
import os
sys.path.append("..")
import json
import time
import openseed_core as Core
import openseed_seedgenerator as Seed
from bottle import route, run, template, request, static_file

@route('/api', method='POST')
def index():
	themessage = request.forms.get("msg")
	appId = ""
	key = ""
	message = ""
	if themessage.split("<::>") > 1:
		appId = themessage.split("<::>")[0]
		key = Account.get_priv_from_pub(appId,"App")
		message = themessage.split("<::>")[1]
		
		decrypted = Seed.simp_decrypt(key,message)
		
		response = Core.message(decrypted)
		
		encrypt = Seed.simp_crypt(key,response)
		
		return encrypt
	else:
		if themessage != None:
			return Core.message(themessage)


run(host='0.0.0.0', port=8670)
