#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
sys.path.append("..")
import openseed_seedgenerator as Seed
from steem import Steem
s = Steem()

import openseed_setup as Settings

settings = Settings.get_settings()

action = ""
steem = ""
accountKey = ""
devId = ""
appId = ""
username = ""
email = ""
passphrase = ""
onetime = ""


def check_db(name,db):
	search = ""
	field = "username"
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()

	
	if db == "users":
		search = "SELECT * FROM `users` WHERE `username` LIKE '"+str(name)+"'"
	if db == "developers":
		search = "SELECT * FROM `developers` WHERE `devName` LIKE '"+str(name)+"'"
	if db == "applications":
		search = "SELECT * FROM `applications` WHERE `appName` LIKE '"+str(name)+"'"
	if db == "profiles":
		search = "SELECT * FROM `profiles` WHERE `id` LIKE '"+str(name)+"'"
	sval = (str(name),)
	mysearch.execute(search)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

def check_appID(appID,devID):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `applications` WHERE appID = %s AND devID = %s"
	val = (str(appID),str(devID),)
	mysearch.execute(search,val)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

def check_devID(name):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `developers` WHERE `devID`= %s"
	val = (str(name),)
	mysearch.execute(search,val)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

def user_from_id(theid):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT username FROM `users` WHERE `userid` = %s"
	val = (str(theid),)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close()
	return str(result).split("'")[1]

def id_from_user(username):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT userid FROM `users` WHERE `username` = %s"
	val = (str(username),)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close()
	return result[0][0].decode()

def accountCheck(username,passphrase):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(username,"users") == 1:
		mysearch = openseed.cursor()
		search = "SELECT userid,email FROM `users` WHERE `username`= %s"
		val = (str(username),)
		mysearch.execute(search,val)
		result = mysearch.fetchall()
		testid = Seed.generate_userid(username,passphrase,str(result[0][1].decode()))
		mysearch.close()
		openseed.close()
		if str(testid) == str(result[0][0].decode()):
			return testid 
		else:
			return "denied" 
	else:
		return "-1"


def create_user(username,passphrase,email):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(username,"users") != 1:
		userid = Seed.generate_userid(username,passphrase,email)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `users` (`userid`,`username`,`email`,`verified`) VALUES (%s,%s,%s,FALSE)"
		val = (str(userid),str(username),str(email))
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return userid
	else:
		return "exists"

def create_developer(devName,contactName,contactEmail,steem):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(devName,"developers") != 1:
		devid = Seed.generate_userid(devName,contactName,contactEmail)
		pubid = Seed.generate_publicid(devid)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `developers` (`devID`,`publicID`,`devName`,`contactName`,`contactEmail`,`steem`) VALUES (%s,%s,%s,%s,%s,%s)"
		val = (str(devid),str(pubid),str(devName),str(contactName),str(contactEmail),str(steem)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return devid
	else:
		return "exists"

def create_app(devID,appName):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(appName,"applications") != 1:
		appID = Seed.generate_userid(devID,devID+AppName+devID,AppName)
		pubID = Seed.generate_publicid(devID,AppName,devID+AppName+devID)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `applications` (`devID`,`appID`,`publicID`,`appName`) VALUES (%s,%s,%s,%s)"
		val = (str(devID),str(appID),str(publicID),str(appName)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return appID
	else:
		return "exists"


def create_profile(theid,data1,data2,data3,data4,data5,thetype):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(theid,"profiles") != 1:
		mycursor = openseed.cursor()
		sql = "INSERT INTO `profiles` (`id`,`data1`,`data2`,`data3`,`data4`,`data5`,`type`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		val = (str(theid),str(data1),str(data2),str(data3),str(data4),str(data5),str(thetype)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return theid
	else:
		return "exists"
	

def get_history(account,apppubIDcount):
	return

def update_history(account,apppubID,data):
	
	return



class Steem:
	def link(username,steemname):
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
		)
		sql = ""
		mycursor = openseed.cursor()
		usersearch = "SELECT * FROM `users` WHERE `username`=%s"
		lval = (str(username),)
		mycursor.execute(usersearch,lval)
		user = str(mycursor.fetchall())
		user = user.split("'")

		code = Seed.generate_userid(username,"terminal","steem")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s"
		sval = (str(code),)
		mycursor.execute(search)
		result = len(mycursor.fetchall())
		if result != 1:
			sql = "INSERT INTO `onetime` (`user`,`onetimecode`,`type`) VALUES (%s,%s,'steem')"
		val = (str(username),str(code))
		mycursor.execute(sql)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return code
	
	def verify(username,code):
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
		)
		sql = ""
		mycursor = openseed.cursor()
		code = Seed.generate_userid(username,random.random(),"steem")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s AND `type` = 'steem'"
		sval = (str(code),)
		mycursor.execute(search,sval)
		result = len(mycursor.fetchall())
		if result != -	1:
			sql = "UPDATE `users` SET `verified` = TRUE WHERE `username` =%s"
			val = (str(username),)
		mycursor.execute(sql,val)
		delete = "DELETE FROM `onetime` WHERE `onetimecode` = %s"
		delval = (str(code),)
		mycursor.execute(delete,delval)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		print("Account Verified")



