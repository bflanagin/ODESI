#!/usr/bin/python
import cgi
import cgitb
import sys
import mysql.connector
import hashlib
import json
import urllib.parse
sys.path.append("..")
from steem import Steem
import openseed_account as Account

import openseed_setup as Settings

settings = Settings.get_settings()

s = Steem()
form = cgi.FieldStorage()

action = form.getvalue("act")
steem = form.getvalue("steem")
accountKey = form.getvalue("key")
devId = form.getvalue('devId')
appId = form.getvalue('appId')
username = form.getvalue('username')
steemname = form.getvalue('steemname')
email = form.getvalue('email')
passphrase = form.getvalue('passphrase')
onetime = form.getvalue('onetime')
userid = form.getvalue('userid')
othername = form.getvalue('othername')
data = form.getvalue('data')

def check_onetime(username,othername):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT codenum FROM onetime WHERE validusers = %s"
	val1 = (username+","+othername,)
	val2 = (othername+","+username,)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())
	mysearch.execute(check,val2)
	result2 = len(mysearch.fetchall())

	if result1 == 1:
		return 1
	elif result2 == 1:
		return 1
	else:
		return 0

def check_chat(username,othername):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT id FROM chat WHERE attendees = %s"
	val1 = (username+","+othername,)
	val2 = (othername+","+username,)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())
	mysearch.execute(check,val2)
	result2 = len(mysearch.fetchall())

	# Below are the 3 states that any chat can be in. 
	# 0 = No key No chat 
	# 1 = Key exists but not chat has started and registration is open
	# 2 = Key exists and Chat has started but registration is open
	# 3 = Chat exists and has started but registration is closed
	if result1 > 0:
		if check_onetime(username,othername) == 1:
			return 2
		else:
			return 3
	elif result2 > 0:
		if check_onetime(username,othername) == 1:
			return 2
		else:
			return 3
	else:
		if check_onetime(username,othername) == 1:
			return 1
		else:
   			return 0

	mysearch.close()
	openseed.close()


def chats(username):
	chatlist = ""
	convolist = []
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	chat = "SELECT attendees,record FROM chat WHERE attendees LIKE %s ORDER BY Id DESC"
	val1 = ("%"+username+"%",)
	mysearch.execute(chat,val1)
	result = mysearch.fetchall()
	for r in result:
		if convolist.count != 0:
			if str(r[0]) not in convolist:
				reverse = str(r[0]).split(",")[1]+","+str(r[0]).split(",")[0]
				if reverse not in convolist:
					convolist.append(str(r[0]))
					chatlist = '{"conversation":"'+str(r[0])+'","message":'+json.dumps(r[1].decode())+'}\n'+chatlist
		else:
			convolist.append(str(r[0]))
			chatlist = '{"conversation":"'+str(r[0])+'","message":'+json.dumps(r[1])+'}\n'+chatlist

	mysearch.close()
	openseed.close()
	return chatlist

def get_chat(userid,username,chatroom,last):
	chat = '{"type":"server","message":"none"}'
	jsoned = chat
	index1 = 0
	index2 = 0
	status1 = ""
	status2 = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT Id,record,attendees,date FROM chat WHERE attendees = %s AND Id > %s ORDER BY Id ASC"
	val1 = (username+","+userid,str(last))
	val2 = (userid+","+username,str(last))
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	mysearch.execute(search,val2)
	result2 = mysearch.fetchall()
	if len(result1) != 0:
		status1 = result1[0][1]
		index1 = result1[0][0]
	if len(result2) != 0:
		status2 = result2[0][1]
		index2 = result2[0][0]
 
	if len(result1) != 0 and len(result2) != 0:
		if index1 > index2:
			jsoned = '{"type":"'+str(result2[0][2]).split(',')[0]+'","message":'+json.dumps(status2.decode())+',"index":"'+str(index2)+'","date":"'+str(result2[0][3])+'"}'
		else:
			jsoned = '{"type":"'+str(result1[0][2]).split(',')[0]+'","message":'+json.dumps(status1.decode())+',"index":"'+str(index1)+'","date":"'+str(result1[0][3])+'"}'
	else:
		if len(result1) != 0:
			jsoned = '{"type":"'+str(result1[0][2]).split(',')[0]+'","message":'+json.dumps(status1.decode())+',"index":"'+str(index1)+'","date":"'+str(result1[0][3])+'"}'
		elif len(result2) != 0:
			jsoned = '{"type":"'+str(result2[0][2]).split(',')[0]+'","message":'+json.dumps(status2.decode())+',"index":"'+str(index2)+'","date":"'+str(result2[0][3])+'"}'

	mysearch.close()
	openseed.close() 

	if status1 != None or status2 != None:
		return jsoned
	else:
		return '{"type":"server","message":"none"}'
	

def send_chat(userid,username,account,data):
	if Account.user_from_id(userid) == username:
		response = '{"type":"server","message":"No data"}'
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
		)
		mysearch = openseed.cursor()
		if len(data) > 0:
			chat = "INSERT INTO chat (attendees,record) VALUES (%s,%s)"
			val1 = (username+","+account,data)
			mysearch.execute(chat,val1)
			openseed.commit()
			mysearch.close()
			openseed.close()
			response = '{"type":"server","message":"updated"}'
	else:
		response = '{"type":"server","message":"denied"}'

	return response


if action == "conversations":
	print(chats(username))
if action == "send_chat":
	print(send_chat(username,othername,data))
if action == "check_chat":
	print(check_chat(username,othername))



