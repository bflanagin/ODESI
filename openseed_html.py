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
	print(themessage)
	if len(themessage.split("<::>")) == 3:
		print("Encrypted message")
		appId = themessage.split("<::>")[0]
		key = Account.get_priv_from_pub(appId,"App")
		message = themessage.split("<::>")[1]
		decrypted = message
		#decrypted = Seed.simp_decrypt(key,message)
		print("From: "+decrypted)
		response = Core.message(decrypted)
		encrypt = Seed.simp_crypt(key,response)	
		#print("Returning: "+Seed.simp_decrypt(key,encrypt))
		return encrypt
	else:
		print("Non-encrypted message")
		if themessage != None:
			return Core.message(themessage)

@route('/upload', method='POST')
def do_upload():
	devPub = request.forms.get('devPub')
	appPub = request.forms.get('appPub')
	cat = request.forms.get('category')
	thefile = request.files.get('data')

	if Account.check_appID(appPub,devPub):
		name, ext = os.path.splitext(thefile.filename)
		save_path = get_save_path_for_category(cat)
		thefile.save(save_path) # appends upload.filename automatically
		if cat == "image":
			info = Utils.png_and_pin(thefile.filename)
		else:
			info = thefile.filename
			
		return info 
	else:
		return 'error'
	
def get_save_path_for_category(category):
	path = ""
	if category == "image":
		path = "openseed/images/source"
	if category == "video":
		path = "openseed/videos/source"
	if category == "game":
		path = "openseed/games"
	if category == "music":
		path = "openseed/music/source"

	return path

@route('/img/<size>/<title>')
def send_image(size,title):
	url = Utils.get_image(True,title,"url",size)
	return static_file(url+'.png', root='openseed/images/'+size+'/', mimetype='image/png')

run(host='0.0.0.0', port=8670)
