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

def groupCheck(name,token):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if check_db(name,"groups") == 1:
		return ("found")


def create_group(name,token,allowed,denied):
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
		
def create_group_invite():

	return()
	
def add_user_to_group():

	return()

def del_user_from_group():

	return()
	
def check_user_roles():

	return()

def set_user_roles():

	return()
