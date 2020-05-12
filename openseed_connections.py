#!/usr/bin/python

import sys
import mysql.connector
import hashlib
import json
import base64
import urllib.parse
sys.path.append("..")
from hive import hive
import openseed_account as Account
import openseed_setup as Settings
import openseed_chat as Chat
import openseed_hive as Hive

settings = Settings.get_settings()

thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
h = hive.Hive(nodes=thenodes)

def get_openseed_connections(account,external = False):
	connections = '{"connections":"none"}'
	ac = 0
	accounts = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	request_search = openseed.cursor()
	search1 = "SELECT userid2,response FROM `connections` WHERE userid1 = %s AND response != 0"
	search2 = "SELECT userid1,response FROM `connections` WHERE userid2 = %s AND response != 0"
	vals = (account,)
	request_search.execute(search1,vals)
	exists1 = request_search.fetchall()
	request_search.execute(search2,vals)
	exists2 = request_search.fetchall()
	
	if len(exists1) != 0:
		ac += len(exists1)
		for u in exists1:
			cname = str(u[0])
			if accounts == "":
				accounts = '{"username":"'+str(cname)+'","linked":'+str(u[1])+','+str(Account.get_profile(str(cname)))+'}'
			else:
				accounts = accounts+',{"username":"'+str(cname)+'","linked":'+str(u[1])+','+str(Account.get_profile(str(cname)))+'}'

	if len(exists2) != 0:
		ac += len(exists2)
		for u in exists2:
			cname = str(u[0])
			if accounts == "":
				accounts = '{"username":"'+str(cname)+'","linked":'+str(u[1])+','+str(Account.get_profile(str(cname)))+'}'
			else:
				accounts = accounts+',{"username":"'+str(cname)+'","linked":'+str(u[1])+','+str(Account.get_profile(str(cname)))+'}'
	if external == False:
		connections = '{"total":'+str(ac)+',"connections":['+accounts.replace("'","\'")+']}'
	else:
		hiveaccount = json.loads(Hive.check_verified(account))["hive"]
		if hiveaccount != "not connected":
			hive = Hive.get_connections(hiveaccount)
			hive_connections = ""
			if len(hive) > 0:
				ac += len(hive)
				for i in hive:
					try:
						json.loads(i)
					except:
						pass
					else:
						stuff = json.loads(i)
						if "username" in stuff and stuff["username"] not in accounts:
							if hive_connections == "":
								hive_connections = i
							else:
								hive_connections = hive_connections+","+i
				if len(accounts) > 0:
					connections = '{"total":'+str(ac)+',"connections":['+accounts.replace("'","\'")+','+hive_connections.replace("'","\'")+']}'
				else:
					connections = '{"total":'+str(ac)+',"connections":['+hive_connections.replace("'","\'")+']}'
		else:
			connections = '{"total":'+str(ac)+',"connections":['+accounts.replace("'","\'")+']}'
	try:
		json.loads(connections)
	except:
		return '{"total":0,"connections":"error"}'
	else:
		return connections

def get_account(account):
	profile = '{"profile":"Not found"}'
	full_account = h.get_account(account)
	if full_account:
		profile = full_account["json_metadata"]
	return(profile)

def profile(token):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	profile = '{"profile":"Not found"}'
	hiveinfo = '{}'
	mysearch = openseed.cursor()
	search = "SELECT data1,data2,data3,data4,data5 FROM `profiles` WHERE `id` = %s"
	val = (theid,)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	if result[0][4]:
		hiveinfo = result[0][4]

	profile = result[0][0]+"','"+result[0][1]+"','"+result[0][2]+"','"+result[0][3]+"','"+hiveinfo
	mysearch.close()
	openseed.close()

	return(profile)


# Requests have three states 1 pending 2 accepted 0 denied. 

def connection_request(token,requestee,response,appPub):
	output = '{"request":"error"}'
	theresponse = 1
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	if response == "request":
		theresponse = 1
	if response == "accept":
		theresponse = 2
	if response == "denied":
		theresponse = 0

	username = json.loads(Account.user_from_id(token))["user"]
	if username != "none":
		request_search = openseed.cursor()
		search = "SELECT * FROM `connections` WHERE userid1 LIKE %s AND userid2 LIKE %s"
		vals_1 = (username,requestee)
		vals_2 = (requestee,username)
		request_search.execute(search,vals_1)
		exists_1 = request_search.fetchall()
		request_search.execute(search,vals_2)
		exists_2 = request_search.fetchall()
		
		# Checks to see if the request is already accepted
		if len(exists_1) == 1 and exists_1[0][3] == 2: 
			output = '{"request":"accepted","to":"'+requestee+'","from":"'+username+'"}'
		elif len(exists_2) == 1 and exists_2[0][3] == 2:
			output = '{"request":"accepted","to":"'+requestee+'","from":"'+username+'"}'	
		# Checks to see if the request is already denied
		elif len(exists_1) == 1 and exists_1[0][3] == 0: 
			output = '{"request":"denied","to":"'+requestee+'","from":"'+username+'"}'
		elif len(exists_2) == 1 and exists_2[0][3] == 0:
			output = '{"request":"denied","to":"'+requestee+'","from":"'+username+'"}'

		# Checks to see if there is no request either direction
		elif len(exists_1) != 1 and len(exists_2) !=1: 
			insert = "INSERT INTO `connections` (`userid1`,`userid2`,`response`) VALUES  (%s,%s,%s)"
			values = (username,requestee,theresponse)
			request_search.execute(insert,values)
			openseed.commit()
			output = '{"request":"sent","to":"'+requestee+'","from":"'+username+'"}'

		# checks to see if the second user has sent a request to the first
		elif len(exists_2) == 1 and int(theresponse) != 1:
  
			update = "UPDATE `connections` SET `response` = %s WHERE userid1 LIKE %s AND userid2 LIKE %s"
			values = (str(theresponse),requestee,username)
			request_search.execute(update,values)
			openseed.commit()
			
			chatroom = Chat.find_attendees(token,requestee+","+username,1,appPub)
			output = '{"request":"accepted","room":'+chatroom+'}'
		# same as above but auto connects users.
		elif len(exists_2) == 1 and int(theresponse) == 1:

			update = "UPDATE `connections` SET `response` = %s WHERE userid1 LIKE %s AND userid2 LIKE %s"
			values = ("2",requestee,username)
			request_search.execute(update,values)
			openseed.commit()
			chatroom = Chat.find_attendees(token,requestee+","+username,1,appPub)
			output = '{"request":"accepted","room":'+chatroom+'}'
		# disallows user from create a second request or updating their own request to others.
		elif len(exists_1) == 1 and int(theresponse) != 0:
			output = '{"request":"exists","to":"'+requestee+'","from":"'+username+'"}'
			
		elif len(exists_1) == 1 and int(theresponse) == 0:
			update = "UPDATE `connections` SET `response` = %s WHERE userid1 LIKE %s AND userid2 LIKE %s"
			values = ("0",requestee,username)
			request_search.execute(update,values)
			openseed.commit()
			output = '{"request":"denied","to":"'+requestee+'","from":"'+username+'"}'
			
		elif len(exists_2) == 1 and int(theresponse) == 0:
			update = "UPDATE `connections` SET `response` = %s WHERE userid2 LIKE %s AND userid1 LIKE %s"
			values = ("0",requestee,username)
			request_search.execute(update,values)
			openseed.commit()
			output = '{"request":"denied","to":"'+requestee+'","from":"'+username+'"}'
	
		request_search.close()
		openseed.close()
	else:
		output = '{"request":"error","log":"bad token"}'

	return output 

# gets requests based on token and limit. Only returns pending requests

def get_requests(token,count):
	requests = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	username = json.loads(Account.user_from_id(token))["user"]
	mysearch = openseed.cursor()
	search = "SELECT * FROM connections WHERE userid2 = %s AND response = 1 LIMIT "+str(count)
	val = (username,)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	if len(result) > 0:
		for a in result:
			theresponse = "pending"
			if a[3] == 0:
				theresponse = "denied"
			if a[3] == 1:
				theresponse = "pending"
			if a[3] == 2:
				theresponse = "accepted"

			if requests == "":
				requests = '{"request":"'+str(a[0])+'","from":"'+str(a[1])+'","response":"'+theresponse+'"}'
			else:
				requests = requests+',{"request":"'+str(a[0])+'","from":"'+str(a[1])+'","response":"'+theresponse+'"}'
	else:
		requests = '{"request":"none"}'
 
	mysearch.close()
	openseed.close()

	return '{"requests":['+str(requests)+']}'


def request_status(token,account):
	status = '{"request":"denied"}'
	jsoned = status
	openseed = mysql.connector.connect(
		host = "localhost",
		user = "openseed",
		password = "b3V4ug3",
		database = "openseed"
		)
	mysearch = openseed.cursor()
	username = json.loads(Account.user_from_id(token))["user"]
	search = "SELECT * FROM connections WHERE userid1 = %s AND userid2 = %s"
	val1 = (username,account)
	val2 = (account,username)
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	mysearch.execute(search,val2)
	result2 = mysearch.fetchall()
	if len(result1) == 1:
		status = result1[0]
	elif len(result2) == 1:
		status = result2[0]
	thestate = "pending"
	if status[3] == 0:
		thestate = "denied"
	if status[3] == 1:
		thestate = "pending"
	if status[3] == 2:
		thestate = "accepted"
	
	jsoned = '{"request":"'+thestate+'","account":"'+account+'"}'

	mysearch.close()
	openseed.close() 

	return jsoned
 
