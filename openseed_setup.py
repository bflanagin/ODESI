#!/usr/bin/python

import sys
import json
import os

sys.path.append("..")

def check_settings_file():
	if os.path.exists("./openseed_settings.json"):
		print("Found file")
		return 1
	else:
		print("No Settings file found")
		return 0

def get_settings():
	settings_file = open("./openseed_settings.json","r")
	settings = json.loads(settings_file.read())
	settings_file.close()
	return settings
	


