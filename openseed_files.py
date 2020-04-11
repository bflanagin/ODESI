#!/usr/bin/python

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import openseed_seedgenerator as Seed
#import steem_get as Get
#import steem_submit as Submit
#import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_setup as Settings
import json
import time
from bottle import route, run, template, get, post, request, static_file

settings = Settings.get_settings()

#@route('/img/<size>/<name>')

@route('/')
def index():
	return template('<b>Hello {{name}}</b>!', name="you need to supply a command")

@route('/upload', method='POST')
def do_upload():
	category = request.forms.get('category')
	md5sum = request.forms.get('md5sum')
	upload = request.files.get('upload')
   
	name, ext = os.path.splitext(upload.filename)

	save_path = get_save_path_for_category(category)
	upload.save(save_path) # appends upload.filename automatically
	return 'OK' 

def get_save_path_for_category(category):
	path = ""
	if category == "image":
		path = "./openseed/images/source"
	if category == "video":
		path = "./openseed/videos/source"
	if category == "game":
		path = "./openseed/games"
	if category == "music":
		path = "./openseed/music/source"
		
	
run(host='0.0.0.0', port=8689)
