#!/usr/bin/python3

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import openseed_seedgenerator as Seed
import openseed_utils as Utils
import hive_get as Get
import hive_submit as Submit
#import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_setup as Settings
import json
import time
import openseed_core as Core
from bottle import route, run, template, request, static_file

settings = Settings.get_settings()




@route('/api', method='POST')
def index():
	themessage = request.forms.get("msg")
	if themessage != None:
		return Core.message(themessage)






run(host='0.0.0.0', port=8670)
