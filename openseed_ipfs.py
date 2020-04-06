#!/usr/bin/python

import subprocess
import sys
import time
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import hive_get as Get
import hive_submit as Submit
import openseed_music as Music
import json

import openseed_setup as Settings

settings = Settings.get_settings()

def pin_and_record(ipfs,author,title,post,img,songtype,genre,songtags,duration):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	mysearch = openseed.cursor()
	search = "SELECT title,duration,genre,date,curation FROM `audio` WHERE `ipfs`='"+str(ipfs)+"'"
	mysearch.execute(search)
	song = mysearch.fetchall()
	result = len(song)
	sql = ""
	values = ""
 
	if result > 1:
		delete = openseed.cursor()
		sql = "DELETE FROM `audio` WHERE ipfs = %s AND date NOT LIKE %s"
		val = (str(ipfs),str(song[0][3]))
		delete.execute(sql,val)
		delete.close()
		openseed.commit()
	if result == None or result == 0:
		mycursor = openseed.cursor() 
		print(title)
		time.sleep(3)
		Submit.like_post(author,post) 
		sql = "INSERT INTO `audio` (`ipfs`,`author`,`title`,`post`,`img`,`type`,`genre`,`tags`,`duration`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		values = (str(ipfs),str(author),str(title),str(post),str(img),str(songtype),str(genre),str(songtags),str(duration))
		mycursor.execute(sql,values)
		openseed.commit()
		subprocess.Popen(["/usr/bin/ipfs","pin","add",str(img)])
		ipfs = subprocess.Popen(["/usr/bin/ipfs","pin","add",str(ipfs)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		#ipfs.wait()
		#stdout, stderr = ipfs.communicate()
		mycursor.close()
		#oggify_and_share(str(stdout).split(" ")[1])
	elif(result == 1):
		if song[0][2] == "NULL" or song[0][2] == "" or song[0][2] == None or song[0][2] == "null":
			updatecursor = openseed.cursor()
			sql = "UPDATE audio SET type = %s, genre = %s, tags = %s, duration = %s WHERE ipfs = %s"
			values = (str(songtype),str(genre),str(songtags),str(duration),str(ipfs))
			updatecursor.execute(sql,values)
			openseed.commit()

	openseed.close()


def oggify_and_share(thehash):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	mysearch = openseed.cursor()
	search = "SELECT ipfs,img FROM `audio` WHERE ipfs ='"+thehash+"'"
	mysearch.execute(search)
	result = mysearch.fetchall()
	process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	stored = str(stdout)
	if str(stderr) == "b''":
		reformat = subprocess.Popen(['ffmpeg', '-n','-i', 'http://142.93.27.131:8080/ipfs/'+thehash, '-vn', '-c:a', 'libvorbis', '-q:a', '4', '/mnt/volume_sfo2_01/openseed/music/'+str(r[0])+'.ogg'])
		reformat.wait()
		add_to_ipfs = subprocess.Popen(['ipfs', 'add' , '/mnt/volume_sfo2_01/openseed/music/'+thehash+'.ogg'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		add_to_ipfs.wait()
		stdout, stderr = add_to_ipfs.communicate()
		updatesql = openseed.cursor()
		sql = "UPDATE audio SET ogg = '"+str(stdout).split(" ")[1]+"' WHERE ipfs ='"+thehash+"'"
		updatesql.execute(sql)
		openseed.commit()
		openseed.close()


