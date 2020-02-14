#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
import json
import subprocess
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
		devID = Seed.generate_userid(devName,contactName,contactEmail)
		pubID = Seed.generate_publicid(devID)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `developers` (`devID`,`publicID`,`devName`,`contactName`,`contactEmail`,`steem`) VALUES (%s,%s,%s,%s,%s,%s)"
		val = (str(devID),str(pubID),str(devName),str(contactName),str(contactEmail),str(steem)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return '{"devID":"'+devID+'","pubID":"'+pubID+'"}'
	else:
		return '{"devID":"exists","pubID":"exists"}'

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
		val = (str(devID),str(appID),str(pubID),str(appName)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return '{"appID":"'+appID+'","pubID":"'+pubID+'"}'
	else:
		return '{"appID":"exists","pubID":"exists"}'


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

def get_status(username):
	status = '{"status":"offline"}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	user = openseed.cursor()
	search = "SELECT * FROM logins WHERE username = %s"
	val = (username,)
	user.execute(search,val)
	result = user.fetchall()
	if len(result) == 1:
		status = '{"username":"'+str(result[0][1]).split("'")[1]+'","date":"'+str(result[0][3])+'","data":'+str(result[0][4]).split("'")[1]+'}'
	user.close()
	openseed.close()

	return status

def get_location(userID,appPubID):
	locale = "0:1"
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	user = openseed.cursor()
	search = "SELECT appPubID,location FROM location WHERE userID = %s"
	val = (userID,)
	user.execute(search,val)
	result = user.fetchall()
	if result >= 0:
		locale = json.dump(result[0])

	return locale

def update_location(userID,appPubID,location):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	user = openseed.cursor()
	search = "SELECT * FROM location WHERE userID = %s"
	val = (userID,)
	user.execute(search,val)
	result = user.fetchall()
	if len(result) == 1:
		update = "UPDATE location SET appPubID = %s location = %s WHERE userID = %s"
		up = (appPubID,location,userID)
		user.execute(update,up)
	else:
		insert = "INSERT INTO location (userID,appPubID,location) VALUES (%s,%s,%s)"
		valin = (userID,appPubID,location)
		user.execute(insert,valin)
	openseed.commit()
	user.close()
	openseed.close()
		
	return 1

def update_status(uid,data):
	username = user_from_id(uid)
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	user = openseed.cursor()
	search = "SELECT * FROM logins WHERE username = %s"
	val = (username,)
	user.execute(search,val)
	result = user.fetchall()
	newdat = '{"location":"'+data["location"]+'","chat":"'+data["chat"]+'"}'
	if len(result) == 1:
		update = "UPDATE logins SET data = %s WHERE username = %s"
		up = (newdat,username)
		user.execute(update,up)
	else:
		insert = "INSERT INTO logins (username,data) VALUES (%s,%s)"
		valin = (username,newdat)
		user.execute(insert,valin)

	update = '{"status":"updated"}'

	openseed.commit()
	user.close()
	openseed.close()

	return update	

def get_history(account,appPubID,count):
	search = ""
	history = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	hist = openseed.cursor()
	if appPubID == "all":
		search = "SELECT data,date FROM `history` WHERE account = %s AND type !=1 ORDER BY date DESC"
		vals = (id_from_user(account),)
		hist.execute(search,vals)
	else:
		search = "SELECT data,date FROM `history` WHERE account = %s AND appID = %s ORDER BY date DESC"
		vals = (id_from_user(account),appPubID)
		hist.execute(search,vals)

	result = hist.fetchall()
	for item in result:
		history += '{"history":"'+str(item[1])+'","item":'+item[0]+'}\n'
	hist.close()
	openseed.close()
	return str("::h::"+history+"::h::")

def update_history(account,history_type,appId,data):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	newdat = data
	
	if history_type == "1":
		newdat = '{"program_start":"'+data["program_start"]+'"}'
	if history_type == "2":
		newdat = '{"program_stop":"'+data["program_stop"]+'"}'
	if history_type == "3":
		newdat = '{"playing":"'+data["playing"]+'"}'
	if history_type == "4":
		newdat = '{"purchase":"'+data["purchase"]+'"}'
	if history_type == "5":
		newdat = '{"download":"'+data["download"]+'"}'
	if history_type == "6":
		newdat = '{"linked":"'+data["linked"]+'"}'

	hist = openseed.cursor()
	check = "SELECT data FROM history WHERE account = %s AND data = %s"
	checked = (account,newdat,)
	hist.execute(check,checked)
	result = hist.fetchall()
	sonj = json.loads(data)
	if "post" not in sonj or len(result) == 0:
		insert = "INSERT INTO history (account,appID,type,data) VALUES (%s,%s,%s,%s)"
		vals = (account,appId,str(history_type),newdat,)
		hist.execute(insert,vals)
		openseed.commit()
		hist.close()
		openseed.close()
		

	return "1"



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
	
	def from_posting_key(username,key,save):
		s.wallet.unlock(user_passphrase=settings["passphrase"])
		user = s.get_account(username)
		keyArray = s.wallet.getPublicKeys()
		username_from_steem = user["name"]
		pubkey_from_steem = user["posting"]["key_auths"][0][0]
		if pubkey_from_steem in keyArray and username == username_from_steem:
			print("Accepted")
			if save == 1:
				return '{"server":"saved"}'
			else:
				s.wallet.removeAccount(username)
				return '{"server":"accepted"}'
		elif username == username_from_steem:
			s.wallet.addPrivateKey(key)
			print("New User")
			return '{"server":"added"}'
		else:
			return '{"server":"denied"}'

