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
import openseed_setup as Settings
import json
import time

settings = Settings.get_settings()

def oggify_and_share(thehash):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
	)
	mysearch = openseed.cursor()
	search = "SELECT ipfs FROM `audio` WHERE ipfs =%s"
	val = (thehash,)
	mysearch.execute(search,val)
	result = mysearch.fetchall()
	if len(result) != 0:
		process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		process.wait()
		stdout, stderr = process.communicate()
		stored = str(stdout)
		if str(stderr) == "b''":
			reformat = subprocess.Popen(['ffmpeg', '-n','-i', 'http://142.93.27.131:8080/ipfs/'+thehash, '-vn', '-c:a', 'libvorbis', '-q:a', '4', '/mnt/volume_sfo2_01/openseed/music/'+thehash+'.ogg'])
			reformat.wait()
			add_to_ipfs = subprocess.Popen(['ipfs', 'add' , '/mnt/volume_sfo2_01/openseed/music/'+thehash+'.ogg'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			add_to_ipfs.wait()
			stdout, stderr = add_to_ipfs.communicate()
			updatesql = openseed.cursor()
			sql = "UPDATE audio SET ogg = %s WHERE ipfs = %s"
			vals = (str(stdout).split(" ")[1],thehash,)
			updatesql.execute(sql,vals)
	openseed.commit()
	openseed.close()
