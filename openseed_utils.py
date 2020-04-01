#!/usr/bin/python

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import openseed_seedgenerator as Seed
#import steem_get as Get
#import steem_submit as Submit
#import leaderboard as LeaderBoard
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

def get_image(source,source_type,size):
	image_url = "No_Image_found"
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
	)
	image = openseed.cursor()

	if source_type == "ipfs":
		search = "SELECT * FROM `images` WHERE ipfs =%s"
		val = (source,)
		image.execute(search,val)
		result = image.fetchall()
		
	elif source_type == "url":
		search = "SELECT * FROM `images` WHERE source =%s"
		val = (source,)
		image.execute(search,val)
		result = image.fetchall()

	if len(result) == 1:
		if size == "medium":
			image_url = result[0][5]
		if size == "low":
			image_url = result[0][4]
		if size == "high":
			image_url = result[0][6]
		if size == "thumbnail":
			image_url = result[0][3]
		if size == "original":
			image_url = result[0][7]
	elif len(result) <= 0:
		recorded = png_and_pin(source)
		if recorded != -1:
			if size == "medium":
				image_url = recorded[5]
			if size == "low":
				image_url = recorded[4]
			if size == "high":
				image_url = recorded[6]
			if size == "thumbnail":
				image_url = recorded[3]
			if size == "original":
				image_url = recorded[7]
			
	openseed.close()

	return image_url

def png_and_pin(url):
	png_returns = -1
	baseDIR = './openseed/images'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
	)
	image = openseed.cursor()
	search = "SELECT ipfs FROM `images` WHERE source =%s"
	val = (url,)
	image.execute(search,val)
	result = image.fetchall()
	
	if len(result) <= 0:
		get = subprocess.Popen(['wget','-T 3','-t 1','-P',baseDIR+"/source",'-nc',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		get.wait()
		stdout, stderr = get.communicate()
		if str(stderr).find("Connection timed out") == -1:
			source = url
			title = url.split("/")[-1]
			source_hash = to_ipfs(baseDIR+"/source/"+title)
			checkfile = subprocess.Popen(['file',baseDIR+"/source/"+title],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			checkfile.wait()
			stdout, stderr = checkfile.communicate()
			if str(stdout).find("GIF") == -1:
				original = subprocess.Popen(['convert',baseDIR+"/source/"+title,baseDIR+"/original/"+title+'.png'])
				original.wait()
				original_hash = to_ipfs(baseDIR+"/original/"+title+'.png')

				high = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '4096x4096',baseDIR+"/high/"+title+'.png'])
				high.wait()
				high_hash = to_ipfs(baseDIR+"/high/"+title+'.png')

				medium = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '2048x2048',baseDIR+"/medium/"+title+'.png'])
				medium.wait()
				medium_hash = to_ipfs(baseDIR+"/original/"+title+'.png')

				low = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '1024x1024',baseDIR+"/low/"+title+'.png'])
				low.wait()
				low_hash = to_ipfs(baseDIR+"/low/"+title+'.png')

				thumbnail = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '128x128',baseDIR+"/thumbnail/"+title+'.png'])
				thumbnail.wait()
				thumbnail_hash = to_ipfs(baseDIR+"/thumbnail/"+title+'.png')

				insert = "INSERT INTO `images` (`ipfs`,`source`,`title`,`thumbnail`,`low`,`medium`,`high`,`original`,`version`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1)"
				data =  (source_hash,url,title,thumbnail_hash,low_hash,medium_hash,high_hash,original_hash,)
				image.execute(insert,data)
		
				png_returns = [source_hash,url,title,thumbnail_hash,low_hash,medium_hash,high_hash,original_hash]
			else:
				png_returns = -1
		else:
			png_returns = 0
	else:
		png_returns = 1
		
	openseed.commit()
	openseed.close()
	
	return png_returns
		
		
def to_ipfs(data):
	add_to_ipfs = subprocess.Popen(['ipfs', 'add' , data],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	add_to_ipfs.wait()
	stdout, stderr = add_to_ipfs.communicate()
	return str(stdout).split(" ")[1]

def data_check(data):
	if data.search("{") and data.search("}"):
		

def password_reset_request(emailaddress):

	return '{"request":"sent"}'

def password_reset(emailaddress,username,passphrase):
	
	newcode = ""
	oldcode = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "openseed"
	)
	u = openseed.cursor()
	search = "SELECT userid FROM `users` WHERE email =%s AND username = %s"
	val = (emailaddress,username)
	u.execute(search,val)
	result = image.fetchall()

	if len(result) == 1:
		newcode = Seed.generate_userid_new(name,passphrase,email)
		oldcode = result[0][0]
		
		userupdate = "UPDATE users SET userid = %s WHERE userid = %s"
		profileupdate = "UPDATE profiles SET id = %s WHERE id = %s"
		history = "UPDATE history SET account = %s WHERE account = %s"
		location = "UPDATE location SET userID = %s WHERE userID = %s"
		val = (newcode,oldcode)
		u.execute(userupdate,val)
		u.execute(profileupdate,val)
		u.execute(history,val)
		u.execute(location,val)
		openseed.commit()
	u.close()
	openseed.close()


