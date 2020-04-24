#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
import json
import subprocess
sys.path.append("..")
import openseed_seedgenerator as Seed
from hive import hive
thenodes = ['anyx.io','api.hive.house','hive.anyx.io','hived.minnowsupportproject.org','hived.privex.io']
s = hive.Hive(nodes=thenodes)

import openseed_setup as Settings

settings = Settings.get_settings()

action = ""
hive = ""
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
		search = "SELECT * FROM `user_tokens` WHERE `username` LIKE '"+str(name)+"'"
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

def check_appID(appPub,devPub):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `applications` WHERE publicID = %s AND devID = %s"
	val = (str(appPub),str(devPub),)
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

def get_priv_from_pub(name):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT devID FROM `developers` WHERE `publicID`= %s"
	val = (str(name),)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close()
	return result[0][0]

def get_pub_from_priv(name):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT publicID FROM `developers` WHERE `devID`= %s"
	val = (str(name),)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close()
	return result[0][0]

def user_from_id(theid):
	return_user = '{"user":"none"}'
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
	if len(result) == 1:
		return_user = '{"user":"'+result[0][0].replace('\x00',"")+'"}'
		
	return return_user

def id_from_user(username):
	return_id = '{"id":"none"}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT token FROM `user_tokens` WHERE `username` = %s"
	val = (str(username),)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close()
	if len(result) == 1:
		return_id = '{"id":"'+result[0][0].replace('\x00',"")+'"}'
	return return_id

def accountCheck(username,passphrase):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(username,"users") == 1:
		mysearch = openseed.cursor()
		search = "SELECT userid,email,hive FROM `users` WHERE `username`= %s"
		val = (str(username),)
		mysearch.execute(search,val)
		result = mysearch.fetchall()

		authsearch = "SELECT auth FROM `upe` WHERE `token` = %s"
		aval = (str(result[0][0]),)
		mysearch.execute(authsearch,aval)
		auth_result = mysearch.fetchall()

		testid = Seed.generate_userid(username,passphrase,str(result[0][1]))
		mysearch.close()
		openseed.close()
		if str(testid) == str(auth_result[0][0]):
			return '{"account":{"token":"'+str(result[0][0])+'","username":"'+username+'"}}' 
		else:
			return '{"account":{"token":"denied"}}' 
	else:
		return '{"account":{"token":"none"}}'


def create_account(username,passphrase,email):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(username,"users") != 1:
		mycursor = openseed.cursor()
		userid = Seed.generate_userid(username,passphrase,email)
		pubid = Seed.generate_publicid(userid)

		findlast = "SELECT token FROM `user_tokens` WHERE 1 LIMIT 1"
		mycursor.execute(findlast)
		lasttoken = mycursor.fetchall()
		newid =""
		if len(lasttoken) <= 0:
			newid = Seed.crypt_key()
		else:
			newid = lasttoken[0][0]

		uid = Seed.generate_usertoken(newid)
		sql = "INSERT INTO `users` (`userid`,`userPub`,`username`,`email`,`verified`) VALUES (%s,%s,%s,%s,FALSE)"
		val = (str(uid),str(pubid),str(username),str(email))
		mycursor.execute(sql,val)

		upe = "INSERT INTO `upe` (`token`,`auth`) VALUES (%s,%s)"
		upe_vals = (str(uid),str(userid))
		mycursor.execute(upe,upe_vals)

		utokens = "INSERT INTO `user_tokens` (`token`,`username`) VALUES (%s,%s)"
		utoken_vals = (str(uid),str(username))
		mycursor.execute(utokens,utoken_vals)

		openseed.commit()
		mycursor.close()
		openseed.close()
		pfile = create_default_profile(uid,username,email)
		return '{"account":{"token":"'+uid+'","username":"'+username+'","profile":'+pfile+'}}'
	else:
		return '{"account":{"username":"exists"}}'


# External users bypass the password and username section of the login, and requires a trust relationship between the providers and OpenSeed
# Steps to complete
# 1. check user existance - done
# 2. check appid existance - done elsewhere
# 3. add to tokens - done
# 4. remove temptoken from temp_data 

def external_user(username,temptoken,network):
	token = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mycursor = openseed.cursor()

	if check_db(username,"users") != 1:
	
		findlast = "SELECT token FROM `user_tokens` WHERE 1 LIMIT 1"
		mycursor.execute(findlast)
		lasttoken = mycursor.fetchall()
		newid =""
		if len(lasttoken) <= 0:
			newid = Seed.crypt_key()
		else:
			newid = lasttoken[0][0]

		utokens = "INSERT INTO `user_tokens` (`token`,`username`) VALUES (%s,%s)"
		utoken_vals = (str(newid),str(username))
		mycursor.execute(utokens,utoken_vals)
		openseed.commit()
		create_default_profile(newid,username,"")
		token = newid
	else:
		token = json.loads(id_from_user(username))["id"]

	return '{"token":"'+token+'","username":"'+username+'"}'	

	
		

def create_default_profile(token,username,email):
	data1 = '{"name":"'+username+'","email":"'+email+'","phone":"","profession":"","company":""}'
	data2 = '{"about":"","profile_img":"","banner":""}'
	data3 = '{"skills":"","interests":""}'
	data4 = '{}'
	data5 = '{}'
	userfriendly = '{"openseed":'+data1+',"extended":'+data2+',"appdata":'+data3+',"misc":"'+data4+'","imports":'+data5+'}'
	set_profile(token,data1,data2,data3,data4,data5,1)

	return userfriendly


def create_creator_account(devName,contactName,contactEmail,account_token):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(devName,"developers") != 1:
		
		mycursor = openseed.cursor()
		account = json.loads(user_from_id(account_token))["user"]
		if account != "none":
			devID = Seed.generate_id(devName,contactName,contactEmail,account)
			pubID = Seed.generate_publicid(devID)
			sql = "INSERT INTO `developers` (`devID`,`publicID`,`devName`,`contactName`,`contactEmail`) VALUES (%s,%s,%s,%s,%s)"
			val = (str(devID),str(pubID),str(devName),str(contactName),str(contactEmail)) 
			mycursor.execute(sql,val)	
			openseed.commit()
			mycursor.close()
			openseed.close()
			return '{"creator_account":{"devID":"'+devID+'","pubID":"'+pubID+'"}}'
		else:
			return '{"creator_account":{"server":"no openseed user found"}}'
	else:
		return '{"creator_account":{"devID":"exists","pubID":"exists"}}'
	

def creator_check(account):

	if check_db(account,"developers") == 1:
		openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
		mysearch = openseed.cursor()
		search = "SELECT devID,publicID FROM `developers` WHERE `openseed` LIKE %s"
		val = (str(account),)
		mysearch.execute(search,val)
		result = mysearch.fetchall()
		mysearch.close()
		openseed.close()
		if len(result) == 1:
			return '{"devID":"'+result[0][0]+'","pubID":"'+result[0][1]+'"}'
		elif len(result) <= 0:
			return '{"devID":"none","pubID":"none"}' 
	else:
		return '{"devID":"none","pubID":"none"}'
		
# Needs developer private ID and a "namespaced" app name something like com.openorchard.testapp#

def create_app(devID,appName):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	pubID = get_pub_from_priv(devID)
	if check_db(appName,"applications") != 1:
		appID = Seed.generate_id(devID,devID+appName,appName,appName+devID)
		pubID = Seed.generate_publicid(appID)
		mycursor = openseed.cursor()
		sql = "INSERT INTO `applications` (`devID`,`appID`,`publicID`,`appName`) VALUES (%s,%s,%s,%s)"
		val = (str(pubID),str(appID),str(pubID),str(appName)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return '{"appID":"'+appID+'","pubID":"'+pubID+'"}'
	else:
		return '{"appID":"exists","pubID":"exists"}'


def set_profile(theid,data1,data2,data3,data4,data5,thetype):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(theid,"profiles") <= 0:
		mycursor = openseed.cursor()
		sql = "INSERT INTO `profiles` (`id`,`data1`,`data2`,`data3`,`data4`,`data5`,`type`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		val = (str(theid),str(data1),str(data2),str(data3),str(data4),str(data5),str(thetype)) 
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close()
		return '{"profile":"created"}'
	else:
		mycursor = openseed.cursor()
		old_profile = json.loads('{'+get_profile(json.loads(get_user_from_id(theid)["user"]))+'}')
		od1 = json.dumps(old_profile["profile"]["openseed"])
		od2 = json.dumps(old_profile["profile"]["extended"])
		od3 = json.dumps(old_profile["profile"]["appdata"])
		od4 = json.dumps(old_profile["profile"]["misc"])
		od5 = json.dumps(old_pofile["profile"]["import"])
		up1 = od1
		up2 = od2
		up3 = od3
		up4 = od4
		up5 = od5
		
		if data1 != "":
			print("updating block 1")
			up1 = data1
		if data2 != "":
			print("updating block 1")
			up2 = data2
		if data3 != "":
			up3 = data3
		if data4 != "":
			up4 = data4
		if data5 != "":
			up5 = data5
		
			
		sql = "UPDATE `profiles` SET data1 = %s, data2 = %s, data3 = %s, data4 = %s, data5 = %s WHERE id = %s"
		val = (str(up1),str(up2),str(up3),str(up4),str(up5),str(theid))
		mycursor.execute(sql,val)	
		openseed.commit()
		mycursor.close()
		openseed.close() 
		return '{"profile":"updated"}'

def get_status(account):
	
	dat = '{"chat":"offline"}'
	status = '{"account":"none","date":"none","data":'+dat+'}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	user = openseed.cursor()
	search = "SELECT * FROM logins WHERE username = %s"
	val = (account,)
	user.execute(search,val)
	result = user.fetchall()
	if len(result) == 1:
		dat = str(result[0][4])
		status = '{"status":{"account":"'+str(result[0][1])+'","date":"'+str(result[0][3])+'","data":'+dat.lower()+'}}'
	

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

def set_location(userID,appPubID,location):
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
		update = "UPDATE location SET appPubID = %s , location = %s WHERE userID = %s"
		up = (appPubID,location,userID)
		user.execute(update,up)
	else:
		insert = "INSERT INTO location (userID,appPubID,location) VALUES (%s,%s,%s)"
		valin = (userID,appPubID,location)
		user.execute(insert,valin)
	openseed.commit()
	user.close()
	openseed.close()
		
	return '{"location":"updated"}'

def set_status(appPub,uid,data):
	
	username = json.loads(user_from_id(uid))["user"]
	if username and username != "none" and username != "None" and username != "None":
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
		newdat = '{"chat":"'+str(data["chat"]).lower()+'"}'
		if len(result) == 1:
			update = "UPDATE logins SET appid = %s , data = %s WHERE username = %s"
			up = (appPub,newdat,username)
			user.execute(update,up)
		else:
			insert = "INSERT INTO logins (appid,username,data) VALUES (%s,%s,%s)"
			valin = (appPub,username,newdat)
			user.execute(insert,valin)

		update = '{"set":{"account":"'+username+'","set_status":'+newdat+'}}'

		openseed.commit()
		user.close()
		openseed.close()

	else:
		update = '{"set":{"account":"'+username+'","status":"error"}}'

	return update	

def get_history(account,apprange,count):
	search = ""
	history = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	hist = openseed.cursor()
	if apprange == "all":
		search = "SELECT data,date FROM `history` WHERE account = %s ORDER BY date DESC"
		vals = (json.loads(id_from_user(account))["id"],)
		hist.execute(search,vals)
	else:
		search = "SELECT data,date FROM `history` WHERE account = %s AND appID = %s ORDER BY date DESC"
		vals = (json.loads(id_from_user(account))["id"],apprange)
		hist.execute(search,vals)

	result = hist.fetchall()
	num = 0
	for item in result:
		
		if history == "":
			history += '{"history":"'+str(item[1])+'","item":'+item[0]+'}'
		else:
			history += ',{"history":"'+str(item[1])+'","item":'+item[0]+'}'
		
		num += 1
	hist.close()
	openseed.close()
	return str('{"history":['+history+']}')

def update_history(account,history_type,appPub,data):
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
		newdat = '{"playing":{"song":"'+data["playing"]["song"]+'","artist":"'+data["playing"]["artist"]+'"}}'
	if history_type == "4":
		newdat = '{"purchase":"'+data["purchase"]+'"}'
	if history_type == "5":
		newdat = '{"download":"'+data["download"]+'"}'
	if history_type == "6":
		newdat = '{"linked":"'+data["linked"]+'"}'
	if history_type == "7":
		newdat = '{"highscore":"'+data["highscore"]+'"}'
	#if history_type == "9":
		#print(data)

	hist = openseed.cursor()
	check = "SELECT data FROM history WHERE account = %s AND data = %s"
	checked = (account,newdat,)
	hist.execute(check,checked)
	result = hist.fetchall()
	sonj = json.loads(newdat)
	if "post" not in sonj or len(result) == 0:
		insert = "INSERT INTO history (account,appID,type,data) VALUES (%s,%s,%s,%s)"
		vals = (account,appPub,str(history_type),newdat,)
		hist.execute(insert,vals)
		openseed.commit()
		hist.close()
		openseed.close()
		

	return '{"history":"updated"}'


def openseed_search(data):
	users = ""
	searchlist = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	no_use_list = ["email",":","name","profession","company"]
	if username not in no_use_list:
		mysearch = openseed.cursor()
		hivesearch = "SELECT userid FROM `users` WHERE hive LIKE %s"
		val = ("%"+data+"%",)
		mysearch.execute(hivesearch,val)
		hive = mysearch.fetchall()
		usersearch = "SELECT id,data1,data5 FROM `profiles` WHERE data1 LIKE %s"
		mysearch.execute(usersearch,val)
		users = mysearch.fetchall()
		for u in users:
			if len(u[0]) > 4:
				userid = u[0]
				accountname = user_from_id(userid)
				userProfile = u[1]
				hiveProfile = '{}'
				if len(u[2]) > 2:
					hiveProfile = u[2]
				if searchlist == "":
					searchlist = '{"account":"'+accountname+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'
				else:
					searchlist = searchlist+',{"account":"'+accountname+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'
		mysearch.close()
		openseed.close()
	
	return '{"search":['+searchlist+']}'

def gps_search(username,cords):
	users = ""
	searchlist = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	#no_use_list = ["NAN:NAN","0.1:0.1","0.000:0.000"," : ","NULL:NULL","None:None","nan:nan","0:1"]
	no_use_list = ["eee:eee"]
	if username not in no_use_list:
		mysearch = openseed.cursor()
		hivesearch = "SELECT data FROM `logins` WHERE username = %s"
		user_lat = 0.00
		user_log = 0.00
		val = (username,)
		mysearch.execute(hivesearch,val)
		user = mysearch.fetchall()
		udat = json.loads(user[0][0])

		#if "location" in udat:
		#	user_location = udat["location"]
		#	user_lat = user_location.split(":")[0]
		#	user_log = user_location.split(":")[1]

		#others = "SELECT username,data FROM `logins` WHERE username NOT LIKE %s AND data LIKE %s"
		#val = ("%"+username+"%",'%"chat":"Online"%')
		others = "SELECT username,data FROM `logins` WHERE username NOT LIKE %s "
		val = (username,)
		mysearch.execute(others,val)
		theothers = mysearch.fetchall()
		searchlist = ""
		for u in theothers:
			odat = json.loads(u[1])
			other_lat = 0.00
			other_log = 0.00

			#if "location" in odat:
			#	other_location = odat["location"]
			#	other_lat = other_location.split(":")[0]
			#	other_log = other_location.split(":")[1]

						
			if float(user_lat) - float(other_lat) < 0.5 and float(user_lat) - float(other_lat) > -0.5:
				if float(user_log) - float(other_log) < 0.5 and float(user_log) - float(other_log) > -0.5:
					userid = id_from_user(u[0])
					psearch = "SELECT id,data1,data5 FROM `profiles` WHERE id = %s"
					pval = (json.loads(userid)["id"],)
					mysearch.execute(psearch,pval)
					profile = mysearch.fetchall()
					if len(profile) == 1:
						userProfile = profile[0][1]
						hiveProfile = profile[0][2]
					else:
						userProfile = '{}'
						hiveProfile = '{}'
					if searchlist == "":
						searchlist = '{"account":"'+u[0]+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'
					else:
						searchlist = searchlist+',{"account":"'+u[0]+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'

		mysearch.close()
		openseed.close()
	
	return '{"gps":['+searchlist+']}'


def get_profile(account):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	profile = '"profile":{}'
	theid = json.loads(id_from_user(account))["id"]

	if theid != "none":
		search = "SELECT data1,data2,data3,data4,data5 FROM `profiles` WHERE `id` = %s"
		sval = (theid,)
		mysearch = openseed.cursor()
		mysearch.execute(search,sval)
		result = mysearch.fetchall()
		data1 = '"None"'
		data2 = '"None"'
		data3 = '"None"'
		data4 = '"None"'
		data5 = '"None"'
		if len(result) == 1:
			if(result[0][0] != "None"):
				data1 = result[0][0]
 
			if(result[0][1] != "None"):
				data2 = result[0][1]
 
			if(result[0][2] != "None"):
				data3 = result[0][2]
 
			if(result[0][3] != "None"):
				data4 = result[0][3]
 
			if(result[0][4] != "None"):
				if(len(result[0][4]) > 1):
					data5 = str(result[0][4]).replace(',"is_public":true',"").replace(',"redirect_uris":["http://142.93.27.131:8675/steemconnect/verify.py"]',"")
				else:
					data5 = '{}'
			else:
				data5 = '{}'

		profile = '"profile":{"openseed":'+data1.replace("\n","")+',"extended":'+data2.replace("\n","")+',"appdata":'+data3.replace("\n","")+',"misc":'+data4.replace("\n","")+',"imports":'+data5.replace("\n","")+'}'

		mysearch.close()
	openseed.close()

	return(profile)

def user_profile_lite(username):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	profile = '"profile":{}'
	theid = json.loads(id_from_user(username))["id"]

	if theid != "none":
		search = "SELECT data1,data2,data3,data4,data5 FROM `profiles` WHERE `id` = %s"
		sval = (theid,)
		mysearch = openseed.cursor()
		mysearch.execute(search,sval)
		result = mysearch.fetchall()
		data1 = '"None"'
		data2 = '"None"'

		if(result[0][0] != "None"):
			data1 = result[0][0]
 
		if(result[0][1] != "None"):
			data2 = result[0][1]

		profile = '"profile":{"openseed":'+data1.replace("\n","")+',"extended":'+data2.replace("\n","")+'}'
	

		mysearch.close()
	openseed.close()

	return(profile)


class hive:
	def link(username,hivename):
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

		code = Seed.generate_userid(username,"terminal","hive")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s"
		sval = (str(code),)
		mycursor.execute(search)
		result = len(mycursor.fetchall())
		if result != 1:
			sql = "INSERT INTO `onetime` (`user`,`onetimecode`,`type`) VALUES (%s,%s,'hive')"
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
		code = Seed.generate_userid(username,random.random(),"hive")
		search = "SELECT * FROM `onetime` WHERE `onetimecode`=%s AND `type` = 'hive'"
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
		#print("Account Verified")
	
	def from_posting_key(username,key,save):
		s.wallet.unlock(user_passphrase=settings["passphrase"])
		user = s.get_account(username)
		keyArray = s.wallet.getPublicKeys()
		username_from_hive = user["name"]
		pubkey_from_hive = user["posting"]["key_auths"][0][0]
		if pubkey_from_hive in keyArray and username == username_from_hive:
			if save == 1:
				return '{"server":"saved"}'
			else:
				s.wallet.removeAccount(username)
				return '{"server":"accepted"}'
		elif username == username_from_hive:
			s.wallet.addPrivateKey(key)
			return '{"server":"added"}'
		else:
			return '{"server":"denied"}'

