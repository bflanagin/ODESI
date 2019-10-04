#!/usr/bin/python

import sys
sys.path.append("..")
import mysql.connector
import socketserver
import account as Account
import steem_get as Get
import steem_submit as Submit
import leaderboard as LeaderBoard
import openseed_music as Music
import json

openseed = mysql.connector.connect(
		host = "localhost",
		user = "",
		password = "",
		database = ""
		)
music = openseed.cursor()
artists = []
search = "SELECT author FROM `audio` WHERE 1"
music.execute(search)
result = music.fetchall()
for artist in result:
	if str(artists).find(artist[0]) == -1:
		print(artist)
		Get.search_artist(artist[0],1000)
		artists.append(artist[0])
		
