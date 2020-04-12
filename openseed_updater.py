#!/usr/bin/python

import subprocess
import sys
import datetime
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import hive_get as Get
import hive_submit as Submit
import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_utils as Utils
import json
import time
import openseed_setup as Settings
import openseed_seedgenerator as Seed

settings = Settings.get_settings()

def update_check(check):
	
	ipfs = mysql.connector.connect(
			host = "localhost",
			user = settings["ipfsuser"],
			password = settings["ipfspassword"],
			database = "ipfsstore"
			)

	openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
			)
	
	if check == "music":
		print("Updating Music")
		music = ipfs.cursor()
		artists = []
		search = "SELECT author FROM `audio` WHERE 1"
		music.execute(search)
		result = music.fetchall()
		for artist in result:
			if str(artists).find(artist[0]) == -1:
				Get.search_music(artist[0],500)
				artists.append(artist[0])
		music.close()
		return(1)
	
	if check == "history":
		print("Updating History")
		users = openseed.cursor()
		userList = []
		search = "SELECT userId,steem FROM `users` WHERE steem IS NOT NULL"
		users.execute(search)
		result = users.fetchall()
		for user in result:
			if str(userList).find(user[1]) == -1:
				Get.search_history(user[1],100)
				userList.append(user[1])
		users.close()
		return(1)

	if check == "oggs":
		print("Updating oggs")
		music = ipfs.cursor()
		search = "SELECT title,ipfs FROM `audio` WHERE ogg IS NULL OR ogg NOT LIKE '_%'"
		music.execute(search)
		result = music.fetchall()
		for oggless in result:
			Utils.oggify_and_share(oggless[1])
		music.close()
		return(1)
		
	if check == "images":
		print("Updating Images")
		img = ipfs.cursor()
		images = []
		search = "SELECT Img,author,post FROM `audio` WHERE 1"
		img.execute(search)
		result = img.fetchall()
		for image in result:
			if len(str(image[0])) == 46 and len(str(image[1])) > 2: 
					Utils.png_and_pin('http://localhost:8080/ipfs/'+image[0])
		img.close()

	if check == "users":
		users = openseed.cursor()
		search = "SELECT username,lastseen,data FROM `logins` WHERE 1"
		users.execute(search)
		update = "UPDATE `logins` SET data = %s WHERE username = %s"
		result = users.fetchall()
		for user in result:
			status = '{"chat":"offline"}'
			username = user[0]
			lastseen = user[1]
			currentdate = datetime.datetime.now()
			currentstate = json.loads(user[2])
			if currentstate["chat"].lower == "online":
				val = (str(status),username,)
				if currentdate.year > lastseen.year:
					users.execute(update,(status,username,))
				elif currentdate.month > lastseen.month:
					users.execute(update,(status,username,))
				elif currentdate.day > lastseen.day:
					users.execute(update,(status,username,))
				elif currentdate.hour > lastseen.hour:
					users.execute(update,(status,username,))
				elif currentdate.minute > lastseen.minute + 10:
					users.execute(update,(status,username,))
		openseed.commit()
		users.close()

	if check == "publify":
		users = openseed.cursor()
		search = "SELECT * FROM `users` WHERE 1"
		users.execute(search)
		update = "UPDATE `users` SET userPub = %s WHERE userId = %s"
		result = users.fetchall()
		for user in result:
			userid = user[1]
			pubid = Seed.generate_publicid(userid)
			val = (str(pubid),userid,)
			if user[2] == None:
				users.execute(update,val)
		openseed.commit()
		users.close()	

	if check == "fix":
		users = openseed.cursor()
		search = "SELECT * FROM `users` WHERE 1"
		users.execute(search)
		update = "UPDATE `users` SET userid = %s, userPub = %s, username = %s, email = %s , steem = %s, verified = %s WHERE userNum = %s"
		result = users.fetchall()
		for user in result:
			print(user)
			userid = user[0]
			d1 = user[1].replace('\x00',"")
			d2 = user[2].replace('\x00',"")
			d3 = user[3].replace('\x00',"")
			d4 = user[4].replace('\x00',"")
			if user[5]:
				d5 = user[5].replace('\x00',"")
			d6 = user[7].replace('\x00',"")
		#	thetype = user[6].replace('\x00',"")  
			val = (d1,d2,d3,d4,d5,d6,userid,)
			users.execute(update,val)

		openseed.commit()
		users.close()	

	ipfs.close()
	openseed.close()

		
if len(sys.argv) > 1:
	update_check(str(sys.argv[1])) 

else:
	print("starting daemon")
	while 1:
		update_check("users")
		update_check("music")
		update_check("oggs")
		update_check("history")
		update_check("images")
		time.sleep(5*60)


		
