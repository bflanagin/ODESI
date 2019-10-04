#!/usr/bin/python

import mysql.connector
import hashlib
import random

from steem import Steem
s = Steem()

action = ""
steem = ""
accountKey = ""
devId = ""
appId = ""
username = ""
email = ""
passphrase = ""
onetime = ""


def check_db(name):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `users` WHERE `username`= %s"
	sval = (str(name))
	mysearch.execute(search,sval)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

def check_appID(appID,devID):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `applications` WHERE `appID`=%s AND `devID`=%s"
	val = (str(appID),str(devID))
	mysearch.execute(search)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

def check_devID(name):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `developers` WHERE `devID`=%s"
	val = (str(name))
	mysearch.execute(search)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	return result

		

def accountCheck(username,passphrase):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	if check_db(username) == 1:
		mysearch = openseed.cursor()
		search = "SELECT userid,email FROM `users` WHERE `username`=%s"
		val = (str(username))
		mysearch.execute(search)
		result = str(mysearch.fetchall())
		result = result.split("'")
		testid = generate_userid(username,passphrase,str(result[3]))
		mysearch.close()
		openseed.close()
		if str(testid) == str(result[1]):
			return testid 
		else:
			return "denied" 
	else:
		return "-1"


def create_user(username,passphrase,email):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	if check_db(username) != 1:
		userid = generate_userid(username,passphrase,email)
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
	user = "",
	password = "",
	database = ""
	)
	if check_db(username) != 1:
		devid = generate_userid(devName,contactName,contactEmail)
		pubid = generate_publicid(devid,contactName,contactEmail)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `developers` (`devID`,`publicID`,`devName`,`contactName`,`contactEmail`,`steem`) VALUES (%s,%s,%s,%s,%s,%s)"
		val = (str(devid),str(pubid),str(devName),str(contactName),str(contactEmail),str(steem)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return userid
	else:
		return "exists"

def create_app(username,passphrase,email):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	if check_db(username) != 1:
		userid = generate_userid(username,passphrase,email)
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

def generate_userid(name,passphrase,email):
	fullstring = name+passphrase+email
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())
	
	count3 = 0	
	while count3 < len(mixer1):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3

def generate_publicid(id):
	random.seed()
	fullstring = random.random()+id+random.random()
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())

	count3 = 0	
	while count3 < len(mixer1):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3[0:8]

class Steem:
	def link(username,steemname):
		openseed = mysql.connector.connect(
		host = "localhost",
		user = "",
		password = "",
		database = ""
		)
		sql = ""
		mycursor = openseed.cursor()
		usersearch = "SELECT * FROM `users` WHERE `username`=%s"
		lval = (str(username))
		mycursor.execute(usersearch,lval)
		user = str(mycursor.fetchall())
		user = user.split("'")

		code = generate_userid(username,"terminal","steem")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s"
		sval = (str(code))
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
		user = "",
		password = "",
		database = ""
		)
		sql = ""
		mycursor = openseed.cursor()
		code = generate_userid(username,random.random(),"steem")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s AND `type` = 'steem'"
		sval = (str(code))
		mycursor.execute(search,sval)
		result = len(mycursor.fetchall())
		if result != -	1:
			sql = "UPDATE `users` SET `verified` = TRUE WHERE `username` =%s"
			val = (str(username))
		mycursor.execute(sql,val)
		delete = "DELETE FROM `onetime` WHERE `onetimecode` = %s"
		delval = (str(code))
		mycursor.execute(delete,delval)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		print("Account Verified")



