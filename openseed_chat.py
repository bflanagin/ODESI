#!/usr/bin/python

import sys
import mysql.connector
import hashlib
import json
import urllib.parse
sys.path.append("..")
from steem import Steem
import openseed_account as Account
import onetime as OneTime
import openseed_setup as Settings
import openseed_seedgenerator as Seed

settings = Settings.get_settings()

thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
s = Steem()

def check_onetime(username,room):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT codenum FROM onetime WHERE room = %s"
	val1 = (room.split("[")[1].split("]")[0],)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())

	if result1 == 1:
		return 1
	else:
		return 0

def create_chatroom(creator,title,userlist,appPub):
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
			)
		room = Seed.generate_publicid(userlist+creator+title)
		chatcreator = openseed.cursor()
		newchat = "INSERT INTO chat (room,title,attendees,record,speaker,appPub) VALUES (%s,%s,%s,%s,'server',%s)"
		vals = (room,title,userlist,'new',appPub)
		chatcreator.execute(newchat,vals)
		newroom = "INSERT INTO chatrooms (creator,title,attendees,room) VALUES (%s,%s,%s,%s)"
		room_vals = (creator,title,userlist,room)
		chatcreator.execute(newroom,room_vals)
		openseed.commit()
		chatcreator.close()	
		openseed.close()
		username= json.loads(Account.user_from_id(creator))["user"]
		newkey = OneTime.store_onetime(1,username,userlist,room)
	
		return '{"type":"server","room":"'+room+'","title":"'+title+'","key":"'+newkey+'"}'
	
def check_chat(userid,room):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	username = json.loads(Account.user_from_id(userid))["user"]
	mysearch = openseed.cursor()
	check = "SELECT Id FROM chat WHERE room = %s"
	val1 = (room.split("[")[1].split("]")[0],)
	val2 = (room.split("[")[1].split("]")[0],)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())
	mysearch.execute(check,val2)
	result2 = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	# Below are the 3 states that any chat can be in. 
	# 0 = No key No chat 
	# 1 = Key exists but not chat has started and registration is open
	# 2 = Key exists and Chat has started but registration is open
	# 3 = Chat exists and has started but registration is closed
	if result1 > 0:
		if check_onetime(username,room) == 1:
			return 2
		else:
			return 3
	elif result2 > 0:
		if check_onetime(username,room) == 1:
			return 2
		else:
			return 3
	else:
		if check_onetime(username,room) == 1:
			return 1
		else:
   			return 0

def get_conversations(token):
	chatlist = ""
	convolist = []
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	username = json.loads(Account.user_from_id(token))["user"]
	mysearch = openseed.cursor()
	chat = "SELECT room,attendees,title,id FROM chat WHERE attendees LIKE %s ORDER BY Id DESC"
	val1 = ("%"+username+"%",)
	mysearch.execute(chat,val1)
	result = mysearch.fetchall()
	for r in result:
		if convolist.count != 0:
			if str(r[0]) not in convolist:
				convolist.append(str(r[0]))
				if chatlist != "":
					chatlist = chatlist+',{"room":"'+str(r[0])+'","attendees":"'+str(r[1])+'","title":"'+str(r[2])+'","index":'+str(r[3])+'}'
				else:
					chatlist = '{"room":"'+str(r[0])+'","attendees":"'+str(r[1])+'","title":"'+str(r[2])+'","index":'+str(r[3])+'}'
		else:
			convolist.append(str(r[0]))
			if chatlist != "":
				chatlist = chatlist+',{"room":"'+str(r[0])+'","attendees":"'+str(r[1])+'","title":"'+str(r[2])+'","index":'+str(r[3])+'}'
			else:
				chatlist = '{"room":"'+str(r[0])+'","attendees":"'+str(r[1])+'","title":"'+str(r[2])+'","index":'+str(r[3])+'}'

	mysearch.close()
	openseed.close()

	return '{"conversations":['+chatlist+']}'

def get_chat_history(userid,room,count,last):
	history = []
	response = '{"chat_history":["none"]}'
	username = json.loads(Account.user_from_id(userid))["user"]

	if room:
		jsoned = ""
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
		)
		mysearch = openseed.cursor()
		search = "SELECT Id,record,attendees,date,speaker FROM chat WHERE room = %s AND Id > %s ORDER BY Id DESC LIMIT "+count
		val1 = (room,str(last))
		mysearch.execute(search,val1)
		result1 = mysearch.fetchall()
		for message in result1:
			status1 = message[1]
			index1 = message[0]
			if jsoned == "":
				jsoned = '{"speaker":"'+str(message[4])+'","room":"'+room+'","message":"'+status1.decode()+'","index":"'+str(index1)+'","date":"'+str(message[3])+'"}'
			else:
				jsoned = '{"speaker":"'+str(message[4])+'","room":"'+room+'","message":"'+status1.decode()+'","index":"'+str(index1)+'","date":"'+str(message[3])+'"},'+jsoned

		response = '{"chat_history":['+jsoned+"]}"
		
	return response

def get_chat(token,chatroom,last):
	chat = '{"chat":{"speaker":"server","room":"'+chatroom+'","message":"none","index":"-1"}}'
	jsoned = chat
	room = ""
	index1 = 0
	status1 = ""
	username = json.loads(Account.user_from_id(token))["user"]
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT Id,record,attendees,date,speaker,appPub FROM chat WHERE room = %s AND Id > %s ORDER BY Id ASC"
	val1 = (chatroom,str(last))
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	if len(result1) != 0:
		status1 = result1[0][1]
		index1 = result1[0][0]
		jsoned = '{"chat":{"speaker":"'+str(result1[0][4])+'","room":"'+chatroom+'","message":"'+status1.decode()+'","index":"'+str(index1)+'","appPub":"'+str(result1[0][5])+'","date":"'+str(result1[0][3])+'"}}'
	mysearch.close()
	openseed.close() 

	if status1 != None:
		chat = jsoned 
	else:
		chat = '{chat:{"speaker":"server","room":"'+chatroom+'","message":"none","index":"-1"}}'
	return chat	

def find_chatroom(chatroom):
	
	room = ""
	title = ""
	attendees = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT title,attendees,date,room FROM chatrooms WHERE room = %s"
	val1 = (chatroom,)
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	mysearch.close()
	openseed.close() 

	if len(result1) != 0:
		room = chatroom
		title = result1[0][0]
		attendees = result1[0][1]

	return [room,title,attendees]	

# Look for rooms based on attendees.
# First narrowing the search using a user token
# Then check provided list against 

def find_attendees(token,userlist,create,appPub):
	room = ""
	title = ""
	found = ""
	username = json.loads(Account.user_from_id(token))["user"]
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT room,title,attendees FROM chatrooms WHERE attendees LIKE %s"
	vals = ("%"+username+"%",)
	mysearch.execute(search,vals)
	result = mysearch.fetchall()
	mysearch.close()
	openseed.close() 
	
	for room in result:
		members = room[2].split(",")
		checkfor = userlist.split(",")
		
		for m in checkfor:
			if m in members:
				members.remove(m)

		if len(members) == 0:
			found = room
			break
	if found == "":
		if int(create) == 1 and len(userlist.split(",")) == 2:
			return create_chatroom(token,"chat",userlist,appPub)
	else:
		key = Seed.get_room_key(token,found[0])
		if key != "":
			output = '{"type":"server","room":"'+found[0]+'","title":"'+found[1]+'","key":"'+key+'"}'
		else:
			output = '{"type":"server","room":"'+found[0]+'","title":"'+found[1]+'","key":"error"}'

		return output
		


def send_chat(userid,chatroom,data,appPub):
	
	roomInfo = find_chatroom(chatroom)
	theRoom = roomInfo[0]
	if len(theRoom) > 3:
		username = json.loads(Account.user_from_id(userid))["user"]
		response = '{"chat_response":{"speaker":"server","message":"denied"}}'
		if username:
			response = '{"chat_response":{"speaker":"server","message":"No data"}}'
			openseed = mysql.connector.connect(
				host = "localhost",
				user = settings["dbuser"],
				password = settings["dbpassword"],
				database = "openseed"
			)
			mysearch = openseed.cursor()
			if len(data) > 0:
				chat = "INSERT INTO chat (room,title,attendees,record,speaker,appPub) VALUES (%s,%s,%s,%s,%s,%s)"
				val1 = (theRoom,roomInfo[1],roomInfo[2],data,username,appPub)
				mysearch.execute(chat,val1)
				openseed.commit()
				mysearch.close()
				openseed.close()
				response = '{"chat_response":{"speaker":"'+username+'","room":"'+theRoom+'","message":"received"}}'
		else:
			response = '{"chat_response":{"speaker":"server","message":"denied"}}'
	else:
		response = '{"chat_response":{"speaker":"server","message":"no room found at '+chatroom+'"}}'

	return response
