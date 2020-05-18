#!/usr/bin/python

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import openseed_seedgenerator as Seed
#import hive_get as Get
#import hive_submit as Submit
import openseed_game as Game
import openseed_music as Music
import openseed_setup as Settings
import json
import time
import email, smtplib, ssl


settings = Settings.get_settings()

def sendmail(receiver,category):
	port = 465
	smtp_server = "smtp.gmail.com"
	sender_email = "no-reply@openorchard.io"  # Enter your address
	receiver_email = receiver  # Enter receiver address
	password = settings["emailpassword"]
	msg = email.message.EmailMessage()
	mess = email_cat(category)
	msg['Subject'] = mess[0]
	msg['From'] = 'no-reply@openorchard.io'
	msg['To'] = receiver
	message = mess[1]
	msg.set_content(message,subtype='html')
	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.send_message(msg)
		server.quit()

	return

def email_cat(cat):
	middle = ""
	subject = ""
	begins = """
		<html>
  		<head></head>
  		<body> 
		"""
	ends = """
		</body>
		</html>
		"""

	if cat == "userreg":
		title = "Verify your OpenSeed User Account"
		middle = """
			<p> Welcome to OpenSeed!</p>
			<p> To finish your registration you can input the code below into the application that requested it.</p> 
			<p> <b> code </b> </p>
			<p> or click on the link to finish registration through the web.</p> """
	if cat == "devreg":
		title = "Verify your OpenSeed Developer Account"
		middle = """
			<p> Welcome brave Developer</p>
			<p> Please input the code below into the application that requested it.</p> 
			<p> <b> code </b> </p>
			<p> or click on this link (link) to finish registration.</p>
			<p> A second email will arrive with your private and public keys, keep them secret, keep them safe. """
	if cat == "devkeymessage":
		title = "Dev keys for your OpenSeed Developer Account"
		middle = """
			<p> Keys for developername </p>
			<p> These keys will be used for various tasks within openseed. It is important you keep them safe.</p> 
			<p> <b> private key </b> </p>
			<p> <b> public key </b> </p>
			 """
	if cat == "appkeymessage":
		title = "App Keys for Application"
		middle = """
			<p> Keys for application </p>
			<p> Your application is registerd and below are the keys needed to access OpenSeed! </p> 
			<p> <b> private key </b> </p>
			<p> <b> public key </b> </p>
			 """
	return [title,begins+middle+ends]

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

def get_image(direct,source,source_type,size):
	print(source," ",source_type)
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
	elif len(result) <= 0 and source != "":

		recorded = png_and_pin(source)
		if recorded != -1:
			record = json.loads(recorded)
			if size == "medium":
				image_url = record["image"]["medium"]
			if size == "low":
				image_url = record["image"]["low"]
			if size == "high":
				image_url = record["image"]["high"]
			if size == "thumbnail":
				image_url = record["image"]["thumbnail"]
			if size == "original":
				image_url = record["image"]["original"]
			
	openseed.close()

	if direct == True:
		if len(result) == 1:
			return result[0][1]
		else:
			return image_url
	else:
		print(image_url)
		return '{"image":{"hash":"'+image_url+'","source":"'+source+'","quality":"'+size+'"}}'

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
	
	from_wget = ""
	source_hash = ""
	
	if len(result) <= 0:

		if data_check(baseDIR+"/source",url) == False:
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
				from_wget = stdout
		else:
			source = url
			title = url
			source_hash = to_ipfs(baseDIR+"/source/"+url)
			checkfile = subprocess.Popen(['file',baseDIR+"/source/"+url],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			checkfile.wait()
			stdout, stderr = checkfile.communicate()
			from_wget = stdout

		if source_hash != "" and str(from_wget).find("GIF") == -1:
			original = subprocess.Popen(['convert',baseDIR+"/source/"+title,baseDIR+"/original/"+source_hash+'.png'])
			original.wait()
			original_hash = to_ipfs(baseDIR+"/original/"+source_hash+'.png')

			high = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '4096x4096',baseDIR+"/high/"+source_hash+'.png'])
			high.wait()
			high_hash = to_ipfs(baseDIR+"/high/"+source_hash+'.png')

			medium = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '2048x2048',baseDIR+"/medium/"+source_hash+'.png'])
			medium.wait()
			medium_hash = to_ipfs(baseDIR+"/original/"+source_hash+'.png')

			low = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '1024x1024',baseDIR+"/low/"+source_hash+'.png'])
			low.wait()
			low_hash = to_ipfs(baseDIR+"/low/"+source_hash+'.png')

			thumbnail = subprocess.Popen(['convert',baseDIR+"/source/"+title,'-resize', '128x128',baseDIR+"/thumbnail/"+source_hash+'.png'])
			thumbnail.wait()
			thumbnail_hash = to_ipfs(baseDIR+"/thumbnail/"+source_hash+'.png')

			insert = "INSERT INTO `images` (`ipfs`,`source`,`title`,`thumbnail`,`low`,`medium`,`high`,`original`,`version`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1)"
			data =  (source_hash,url,title,thumbnail_hash,low_hash,medium_hash,high_hash,original_hash,)
			image.execute(insert,data)
		
			png_returns = '{"image":{"source":"'+source_hash+'","url":"'+url+'","title":"'+title+'","thumbnail":"'+thumbnail_hash+'","low":"'+low_hash+'","medium":"'+medium_hash+'","high":"'+high_hash+'","original":"'+original_hash+'"}}'
		else:
			png_returns = -1
	else:
		png_returns = 1
		
	openseed.commit()
	openseed.close()
	
	return png_returns
		
		
def to_ipfs(data):
	add_to_ipfs = subprocess.Popen(['ipfs', 'add' , data],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	add_to_ipfs.wait()
	stdout, stderr = add_to_ipfs.communicate()
	if len(str(stdout).split(" ")) > 1: 
		return str(stdout).split(" ")[1]
	else:
		return ""

def data_check(path,filename):
	dirlist = os.listdir(path)
	if filename in dirlist:
		return True
	else: 
		return False

# The tasks for this function are as follows
# 1. Find user in user database
# 2. Generate and store new token for user along with username
# 3. Populate upe database with token and authkey 
# 4. Move users db authkey to new token

def new_token_switch():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)
	tokenupdate = openseed.cursor()
	search = "SELECT userid,username FROM `users` WHERE 1"
	tokenupdate.execute(search)
	usersAndIds = tokenupdate.fetchall()
	for user in usersAndIds:
		auth = user[0]
		username = user[1].replace("\t","")
		checktokens = "SELECT token FROM `user_tokens` WHERE username = %s"
		val = (username,)
		tokenupdate.execute(checktokens,val)
		if len(tokenupdate.fetchall()) <= 0:
			findlast = "SELECT token FROM `user_tokens` WHERE 1 LIMIT 1"
			tokenupdate.execute(findlast)
			lasttoken = tokenupdate.fetchall()
			newid =""
			if len(lasttoken) <= 0:
				print("Creating token")
				newid = Seed.crypt_key()
			else:
				newid = lasttoken[0][0]
		tokes = Seed.generate_usertoken(newid)
		insert = "INSERT INTO user_tokens (token,username) values(%s,%s)"
		insvals = (tokes,username)
		tokenupdate.execute(insert,insvals)
		token_share = "INSERT INTO upe (token,auth) values(%s,%s)"
		tsvals = (tokes,auth)
		tokenupdate.execute(token_share,tsvals)
		move_over = "UPDATE users SET userid = %s WHERE userid = %s"
		movals = (tokes,auth)
		tokenupdate.execute(move_over,movals)
	
	openseed.commit()
	tokenupdate.close()
	openseed.close()

def update_everything():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)

	u = openseed.cursor()
	search = "SELECT * FROM `upe` WHERE 1"
	u.execute(search)
	result = u.fetchall()

	for task in result:
		newcode = task[0]
		oldcode = task[1]
		
		profileupdate = "UPDATE profiles SET id = %s WHERE id = %s"
		history = "UPDATE history SET account = %s WHERE account = %s"
		location = "UPDATE location SET userID = %s WHERE userID = %s"
		chatrooms = "UPDATE chatrooms SET creator = %s WHERE creator = %s"
		val = (newcode,oldcode)
		u.execute(profileupdate,val)
		u.execute(history,val)
		u.execute(location,val)
		u.execute(chatrooms,val)
		openseed.commit()

	u.close()
	openseed.close()


def password_reset_request(emailaddress):

	return '{"request":"sent"}'

def password_reset(emailaddress,username,passphrase):
	
	newcode = ""
	oldcode = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)
	u = openseed.cursor()
	search = "SELECT userid FROM `users` WHERE email =%s AND username = %s"
	val = (emailaddress,username)
	u.execute(search,val)
	result = u.fetchall()

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


def keytest(message):
	key = Seed.crypt_key()
	key2 = Seed.crypt_key()
	encrypted = Seed.simp_crypt(key,message)
	print("sample using supplied key: "+Seed.simp_decrypt(key,encrypted))
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)
	u = openseed.cursor()
	search = "SELECT code FROM `onetime` WHERE 1"
	u.execute(search)
	result = u.fetchall()
	print("attempts using existing keys: blanks are good")
	for test in result:
		decrypted = Seed.simp_decrypt(test[0],encrypted)
		print("attempt: "+decrypted)
		if decrypted == message:
			print("success - which is bad")
			break
	print("test with random values")
	while 1:
		decrypted = Seed.simp_decrypt(Seed.crypt_key(),encrypted)
		if decrypted == message:
			print("success - which is bad")
			break


def import_hive_profile(token,username):
	
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)
	
def ipfs_pin_request(thehash,thetype,reference):

	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
	)

def openseed_search(data,category = "user",count = 20):
	users = ""
	searchlist = ""
	search_return_template = '"search":'
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()	
	no_use_list = ["email",":","name","profession","company"]
	if data not in no_use_list:
		if category == "user":
			search_return_template = 'user_search'
			hivesearch = "SELECT userid FROM `users` WHERE hive LIKE %s LIMIT %s"
			val = ("%"+data+"%",int(count),)
			mysearch.execute(hivesearch,val)
			hive = mysearch.fetchall()
			usersearch = "SELECT id,data1,data5 FROM `profiles` WHERE data1 LIKE %s LIMIT %s"
			mysearch.execute(usersearch,val)
			users = mysearch.fetchall()
			for u in users:
				if len(u[0]) > 4:
					userid = u[0]
					accountname = user_from_id(userid)
					userProfile = u[1]
					hiveProfile = '{}'
					if len(u[2]) > 2:
						hiveProfile = u[2]
					if searchlist == "":
						searchlist = '{"account":"'+accountname+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'
					else:
						searchlist = searchlist+',{"account":"'+accountname+'","profile":'+userProfile+',"hive":'+hiveProfile+'}'
		if category == "app":
			search_return_template = 'app_search'
			appssearch = "SELECT * FROM `applications` WHERE appName LIKE %s LIMIT %s"
			val = ("%"+data+"%",str(count),)
			mysearch.execute(hivesearch,val)
			apps = mysearch.fetchall()
			profilesearch = "SELECT id,data1,data5 FROM `profiles` WHERE data1 LIKE %s LIMIT %s"
			mysearch.execute(usersearch,val)
			appprofile = mysearch.fetchall()
			for u in appprofile:
				if len(u[0]) > 4:
					appid = u[0]
					appProfile = u[1]
					if searchlist == "":
						searchlist = '{"app":"'+accountname+'","profile":'+appProfile+'}'
					else:
						searchlist = searchlist+',{"app":"'+accountname+'","profile":'+appProfile+'}'
		
	
	mysearch.close()
	openseed.close()
	
	return '{"'+search_return_template+'":['+searchlist+']}'

