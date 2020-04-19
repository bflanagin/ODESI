#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
#import hive_submit as Submit
import openseed_setup as Settings
settings = Settings.get_settings()

#### These functions will need to be changed to match the current versions. We can move leaderboard to history and use filters to find just highscores based on apps #####
#### Save functions can also be moved to the app_data tables. The main purpose of this area will be for simple servers and other tools that could be a boone to any real time activities

####

def update_leaderboard(devID,appID,user,data):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	scoresearch = openseed.cursor()
	search = "SELECT * FROM `history` WHERE `devID` = %s AND `appID` = %s AND `username` = %s AND `data` = %s `type` = '99'"
	vals = (str(devID),str(appID),str(user),str(data))
	scoresearch.execute(search,vals)
	result = len(scoresearch.fetchall())
	if result == 0:
		sql = "INSERT INTO `history` (`devID`,`appID`,`username`,`data`, `type`) VALUES (%s,%s,%s,%s,"99")"
		vals = (str(devID),str(appID),str(user),str(data))
		scoresearch.execute(sql,vals)	
		openseed.commit()
		Submit.leaderboard(devID,appID,user,data)
	scoresearch.close()
	openseed.close()
	return "1"

def get_leaderboard(devID,appID):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	scoresearch = openseed.cursor()
	output = ""
	search = "SELECT username,data FROM `history` WHERE `type` = '99' AND `devID` = '"+str(devID)+"' AND `appID` = '"+str(appID)+"'"
	scoresearch.execute(search)
	result = scoresearch.fetchall()
	for score in result:
		output = str(score)+","+output
	scoresearch.close()
	openseed.close()
	return str(output)

def save_game(devID,appID,token,data):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	save = openseed.cursor()
	search = "SELECT * FROM `app_data_priv` WHERE `devID` = %s AND `appID` = %s AND `data` = %s"
	vals = (str(devID),str(appID),str(user),str(data))
	save.execute(search,vals)
	result = len(scoresearch.fetchall())
	if result == 0:
		sql = "INSERT INTO `app_data_priv` (`devID`,`appID`,`data`) VALUES (%s,%s,%s,%s,'99')"
		vals = (str(devID),str(appID),str(user),str(data))
		save.execute(sql,vals)	
		openseed.commit()
	save.close()
	openseed.close()

def get_saved_games(devID,appID,token):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	save = openseed.cursor()
	search = "SELECT * FROM `app_data_priv` WHERE `devID` = %s AND `appID` = %s AND `data` = %s"
	vals = (str(devID),str(appID),str(user),str(data))
	save.execute(search,vals)
	result = len(scoresearch.fetchall())
	if result == 0:
		sql = "INSERT INTO `app_data_priv` (`devID`,`appID`,`data`) VALUES (%s,%s,%s,%s,'99')"
		vals = (str(devID),str(appID),str(user),str(data))
		save.execute(sql,vals)	
		openseed.commit()
	save.close()
	openseed.close()


