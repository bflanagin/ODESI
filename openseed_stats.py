#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import openseed_setup as Settings
settings = Settings.get_settings()

def get_stats(user,steem):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()

	return

def get_listens(song):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	os = openseed.cursor()
	search = "SELECT * FROM `history` WHERE  `type` = 3 AND `data` = '%"+str(data)+"%'"
	os.execute(search)
	totalplays = len(os.fetchall())
	

	openseed.close()
	return '{"total":"'+totalplays+'"}'

def get_posts(steem,db):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()
	return

def get_connections(user,db):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()
	return

def get_likes(steem,db):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()
	return

def get_comments(steem,db):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()	
	return

def get_post(steem,db):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	search = openseed.cursor()



	openseed.close()
	return
