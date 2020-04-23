#!/usr/bin/python3

import subprocess
import sys
import os
sys.path.append("..")
import json
import time
import openseed_core as Core
from bottle import route, run, template, request, static_file

@route('/api', method='POST')
def index():
	themessage = request.forms.get("msg")
	if themessage != None:
		return Core.message(themessage)


run(host='0.0.0.0', port=8670)
