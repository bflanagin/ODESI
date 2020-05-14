#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
import json
import subprocess
sys.path.append("..")
import openseed_seedgenerator as Seed
import openseed_account as Account
import openseed_connections as Connections

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
	if Account.check_db(name,"groups") == 1:
		return 1


def create_group(token,title,allowed,denied,appPub):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	username = json.loads(Account.user_from_id(token))["user"]
	if Account.check_db(title,"groups") != 1:
		mycursor = openseed.cursor()

		findlast = "SELECT token FROM `user_tokens` WHERE 1 LIMIT 1"
		mycursor.execute(findlast)
		lasttoken = mycursor.fetchall()
		newid =""
		if len(lasttoken) <= 0:
			newid = Seed.crypt_key()
		else:
			newid = lasttoken[0][0]

		uid = Seed.generate_usertoken(newid)
		sql = "INSERT INTO `groups` (`id`,`title`,`owner`,`allowed`,`denied`,`permissions`) VALUES (%s,%s,%s,%s,%s,%s)"
		val = (str(uid),str(title),str(username),str(allowed),str(denied),str('{"admin":"'+str(username)+'"}'))
		mycursor.execute(sql,val)

		utokens = "INSERT INTO `user_tokens` (`token`,`username`) VALUES (%s,%s)"
		utoken_vals = (str(uid),str(title))
		mycursor.execute(utokens,utoken_vals)

		openseed.commit()
		mycursor.close()
		openseed.close()
		
		email = "no@email.com"
		pfile = create_default_profile(uid,name,email)
		for a in allowed:
			Connections.connection_request(uid,a,2,"request",appPub)
		for d in denied:
			Connections.connection_request(uid,d,2,"denied",appPub)
		
		return '{"group":{"token":"'+uid+'","title":"'+name+'","allowed":"'+allowed+'","denied":"'+denied+'"}}'
	else:
		return '{"group":{"title":"exists"}}'
		
def group_list(token):
	response = '{"group_list":[]}'
	groups = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)	
	mycursor = openseed.cursor()
	owner = json.loads(Account.user_from_id(token))["user"]
	find = "SELECT title,allowed,denied FROM `groups` WHERE `owner` = %s OR `allowed` LIKE % %s %"
	mycursor.execute(find)
	results = mycursor.fetchall()
	for group in results:
		if groups == "":
			groups += '{"group":"title":"'+group[0]+'","allowed":"'+group[1]+'","denied":"'+group[2]+'"}'
		else:
			groups += ',{"group":"title":"'+group[0]+'","allowed":"'+group[1]+'","denied":"'+group[2]+'"}'
	response = '{"group_list":["'+groups+'"]}'
	
	openseed.commit()
	mycursor.close()
	openseed.close()
	
	return response
	
def group_list_users(token,title):
	response = '{"user_list":"group":"error","allowed":[],"denied":[]}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()
		find = "SELECT title,allowed,denied FROM `groups` WHERE `title` = %s AND owner = %s OR `allowed` LIKE % %s %"
		vals = (title,username,username,)
		mycursor.execute(find,vals)
		results = mycursor.fetchall()
		if len(results) == 1:
			response = '{"user_list":"group":"'+results[0][0]+'","allowed":["'+results[0][1]+]'","denied":"'[+results[0][2]+]'"}'
		
	openseed.commit()
	mycursor.close()
	openseed.close()

	return response
		
def delete_group(token,title,appPub):
	response = '{deleted_group:{"error":"not the owner"}}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	username = json.loads(Account.user_from_id(token))["user"]
	if Account.check_db(title,"groups") != 1:
		mycursor = openseed.cursor()
		sql = "DELETE FROM `groups` WHERE title = %s AND owner = %s"
		val = (title,username)
		
	openseed.commit()
	mycursor.close()
	openseed.close()
	
	return response
			
def add_user_to_group(token,title,user):
	response = '{"group_add":{"user":"error"}}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()
		owner = json.loads(Account.user_from_id(token))["user"]
		find = "SELECT allowed,denied FROM `groups` WHERE `title` = %s AND `owner` = %s"
		vals = (title,owner,)
		mycursor.execute(find,vals)
		results = mycursor.fetchall()[0]
		allowed = results[0]
		denied = results[1]
		newdenied = []
		
		for a in allowed.split(","):
			if user == a:
				response = '{"group_add":{"user":"exists"}}'
				break
				
		for d in denied.split(",");
			if user != d:
				newdenied.append(d)
		
		adding = "UPDATE groups SET allowed = %s, denied = %s WHERE owner = %s AND title = %s"
		vals = (allowed+","+user,newdenied.join(","),owner,title)
		mycursour.execute(adding,vals)
		response = '{"group_add":{"user":"added"}}'
	openseed.commit()
	mycursor.close()
	openseed.close()

	return response

def del_user_from_group(token,title,user):
	response = '{"group_del":{"user":"error"}}'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()
		owner = json.loads(Account.user_from_id(token))["user"]
		find = "SELECT allowed,denied FROM `groups` WHERE `title` = %s AND `owner` = %s"
		vals = (title,owner,)
		mycursor.execute(find,vals)
		results = mycursor.fetchall()[0]
		allowed = results[0]
		denied = results[1]
		newallowed = []
		
		for a in denied.split(","):
			if user == a:
				response = '{"group_del":{"user":"exists"}}'
				break
				
		for d in allowed.split(",");
			if user != d:
				newdenied.append(d)
		
		adding = "UPDATE groups SET allowed = %s, denied = %s WHERE owner = %s AND title = %s"
		vals = (newallowed.join(","),denied+","+user,owner,title)
		mycursour.execute(adding,vals)
		response = '{"group_del":{"user":"denied"}}'
		
	openseed.commit()
	mycursor.close()
	openseed.close()

	return response
	
def check_user_roles(group,user):
	
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()	
		
	openseed.commit()
	mycursor.close()
	openseed.close()

	return ()

def set_user_roles(token,group,user):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()	
		
	openseed.commit()
	mycursor.close()
	openseed.close()

	return ()


def create_group_invite(token,group):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if Account.check_db(title,"groups") == 1:
		mycursor = openseed.cursor()	
		
	openseed.commit()
	mycursor.close()
	openseed.close()

	return ()
