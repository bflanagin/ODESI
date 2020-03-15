#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import steem_submit as Submit
import openseed_setup as Settings
settings = Settings.get_settings()

def update_leaderboard(devID,appID,user,data,steem,postingkey):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	scoresearch = openseed.cursor()
	search = "SELECT * FROM `leaderboard` WHERE `devID` = '"+str(devID)+"' AND `appID` = '"+str(appID)+"' AND `username` ='"+str(user)+"' AND `data` = '"+str(data)+"'"
	scoresearch.execute(search)
	result = len(scoresearch.fetchall())
	if result == 0:
		sql = "INSERT INTO `leaderboard` (`devID`,`appID`,`username`,`data`) VALUES ('"+str(devID)+"','"+str(appID)+"','"+str(user)+"','"+str(data)+"')"
		scoresearch.execute(sql)	
		openseed.commit()
		Submit.leaderboard(devID,appID,user,data,steem,postingkey)
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
	search = "SELECT username,data FROM `leaderboard` WHERE `devID` = '"+str(devID)+"' AND `appID` = '"+str(appID)+"'"
	scoresearch.execute(search)
	result = scoresearch.fetchall()
	for score in result:
		output = str(score)+","+output
	scoresearch.close()
	openseed.close()
	return str(output)

