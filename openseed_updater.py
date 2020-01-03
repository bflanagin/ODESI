#!/usr/bin/python

import subprocess
import sys
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import steem_get as Get
import steem_submit as Submit
import leaderboard as LeaderBoard
import openseed_music as Music
import json
import time
import openseed_setup as Settings

settings = Settings.get_settings()

def update_check(check):
	
	openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["ipfsuser"],
			password = settings["ipfspassword"],
			database = "ipfsstore"
			)
	
	if check == "music":
		music = openseed.cursor()
		artists = []
		search = "SELECT author FROM `audio` WHERE 1"
		music.execute(search)
		result = music.fetchall()
		for artist in result:
			if str(artists).find(artist[0]) == -1:
				print(artist[0])
				Get.search_artist(artist[0],100)
				artists.append(artist[0])
		music.close()
		return(1)
		
	if check == "images":
		img = openseed.cursor()
		images = []
		search = "SELECT Img,author,post FROM `audio` WHERE 1"
		img.execute(search)
		result = img.fetchall()
		for image in result:
			if len(str(image[0])) == 46 and len(str(image[1])) > 2: 
					print(str(image[0]),str(image[1]))
					get = subprocess.Popen(['wget','-t 10','-nc','http://localhost:8080/ipfs/'+image[0]])
					#get.wait()
		img.close()

	openseed.close()
		
if len(sys.argv) > 1:
	update_check(str(sys.argv[1])) 

else:
	print("starting daemon")
	while 1:
		update_check("music")
		time.sleep(5*60)


		
