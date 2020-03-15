#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import openseed_setup as Settings
settings = Settings.get_settings()

def get_appdata(mode,appID,data):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()

	openseed.close()

	return

def set_appdata(mode,appID,data,update)
