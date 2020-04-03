#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import openseed_setup as Settings
import openseed_seedgenerator as Seed
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

def set_appdata(mode,appID,data,update):

	return

# We get the application public id and the applications private token and check to see if they match. If they do we create a token for the app to send to the user

def create_webapp_token(dpub,apub,verification):
	temptoken = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()
	find = "SELECT publicID FROM `applications` WHERE appID = %s AND devID = %s"
	vals = (verification,dpub)
	search.execute(find,vals)
	result = search.fetchall()
	if len(result) == 1:
		if result[0][0] == apub:
			temptoken = '{"'+apub+'":"'+Seed.generate_usertoken(dpub+apub)+'"}'
			add_token = "INSERT INTO `temp_data` (`devID`, `appID`, `data`) VALUES (%s,%s,%s)"
			token_vals = (dpub,apub,temptoken)
			openseed.commit()

	search.close()		
	openseed.close()

	return temptoken

def get_webapp_token(token,username,appPub):
	output = '{"appPub":"none","token":"error"}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()
	the_token = '{"'+appPub+'":"'+token+'"}'
	find = "SELECT * FROM `temp_data` WHERE data = %s"
	val = (the_token,)
	search.execute(find,val)
	result = search.fetchall()

	if len(result) == 1:
		
		output = '{"appPub":"'+appPub+'","token":"'token'"}'
	
	
	
	return output






