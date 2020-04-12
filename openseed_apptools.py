#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import openseed_account as Account
import openseed_setup as Settings
import openseed_seedgenerator as Seed
settings = Settings.get_settings()


# Get app data from public app data 
# This data is organized into developer and application with little or no regard to the data that they store
# However, we require the data be stored in json formated units for easy searching through database returns. 
# We do not have a standard format for this area as we want the developer to feel like they can use it for whatever they feel like.
# Steps for future function: 1) search app and developer id and return results 2) search results for things that match data. 

def get_appdata(mode,appID,data):

	table = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
		if mode == "priv":
			table = "app_data_priv"
		else:
			table = "app_data_pub"		
	try:
		json.loads(data)
	except:
		return '{"server":"not json"}'
	else:
		search = openseed.cursor()
		find = "SELECT * FROM `"+table+"` WHERE appID = %s"
		vals = (appID,)
		search.execute(find,vals)
		result = search.fetchall()

		for t in result:
			print(t)

	search.close()
	openseed.close()

	return

def set_appdata(mode,appID,data,update):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
		if mode == "priv":
			table = "app_data_priv"
		else:
			table = "app_data_pub"
	try:
		json.loads(data)
	except:
		return '{"server":"not json"}'
	else:
		search = openseed.cursor()
		insert = "INSERT INTO `"+table+"` (`appID`,`data`) VALUES (%s,%s)"
		vals = (appID,data)
		search.execute(insert,vals)
	
	
	openseed.commit()
	search.close()
	openseed.close()

	return

# We get the application public id and the applications private token and check to see if they match. If they do we create a token for the app to send to the user

def create_webapp_token(dpub,apub,username,verification):
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
			temptoken = '{"username":"'+username+'","'+apub+'":"'+Seed.generate_usertoken(dpub+apub)+'"}'
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
	the_token = '{"username":"'+username+'","'+appPub+'":"'+token+'"}'
	find = "SELECT * FROM `temp_data` WHERE data = %s"
	val = (the_token,)
	search.execute(find,val)
	result = search.fetchall()

	token = json.loads(Account.id_from_username(username))["id"]

	if token != "none" and len(result) == 1:
		output = '{"appPub":"'+appPub+'","token":"'token'"}'
	elif token == "none":
		Account.create_user
	
	
	return output






