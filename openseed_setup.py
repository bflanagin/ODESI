#!/usr/bin/python3

import sys
import json
import os
import mysql.connector

sys.path.append("..")

def check_settings_file():
	if os.path.exists("./openseed_settings.json"):
		print("Found file")
		return 1
	else:
		print("No Settings file found")
		return 0

def get_settings():
	settings_file = open("./openseed_settings.json","r")
	settings = json.loads(settings_file.read())
	settings_file.close()
	return settings
	
def save_settings(data):
	settings_file = open("./openseed_settings.json","w")
	settings = {"serverkey":data[0],"steemaccount":data[1],"passphrase":data[2],"dbuser":data[3],"dbpassword":data[4],"ipfsuser":data[5],"ipfspassword":data[6]}
	settings_file.write()
	settings_file.close()

def create_node():
	print("\n")
	print("Welcome to the OpenSeed Setup. Please read the next dialogs carefully.\nThese settings will be writen to a openseed_settings.json for reference later.")
	print("\n(Press any key to continue)")
	input()
	print("\nThese next two options are for if you intend to post to the steem blockchain on your own behalf or on behalf of others.\n\
You may leave these blank if you are unsure or if you would rather the main node to handle chain operations.\n")

	steemaccount = input("Please enter steemaccount: ")
	passphrase = input("Please enter phasphrase to unlock local keychain: ")
	print("\nNext up we will need to setup databases to store and retrieve information. \n")
	LocaladminID = input("Enter the account name of the mysql database admin: ")
	LocaladminPassword = input(LocaladminID+"'s password: ")
	print("\n\nCreating OpenSeed database using supplied account.")
	# Create OpenSeed database
	create_database(LocaladminID,LocaladminPassword,"openseed")
	create_database(LocaladminID,LocaladminPassword,"openseed_sync")
	print("\n\nCreating ipfs database using supplied account.")
	# Create ipfs database
	create_database(LocaladminID,LocaladminPassword,"ipfs")

	print("\n\nNow we will create the users to access the databases \n \n") 
	dbuser = input("Please enter the username for the openseed database: ")
	dbpassword = input("Now enter the password for "+dbuser+" :")
	print("\nSetting up user and rights to the database")
	#Setup rights
	create_openseed_users(LocaladminID,LocaladminPassword,dbuser,dbpassword,"openseed")
	create_openseed_users(LocaladminID,LocaladminPassword,dbuser,dbpassword,"openseed_sync")
	print("\nNow enter the desired username for the ipfs centric database \n")
	ipfsuser = input("IPFS database user: ")
	ipfspassword = input(ipfsuser+"'s password: ")
	print("\nSetting up user and rights to the database")
	create_openseed_users(LocaladminID,LocaladminPassword,dbuser,dbpassword,"ipfs")

def create_database(username,password,database):
	db = mysql.connector.connect(
			host = "localhost",
			user = username,
			password = password
			)
	cursor = db.cursor()
	create = "CREATE DATABASE IF NOT EXISTS "+database+" CHARACTER SET utf8 COLLATE utf8_unicode_ci "
	cursor.execute(create)
	cursor.close()
	return 1	

def create_openseed_users(admin,adminPassword,username,password,database):
	db = mysql.connector.connect(
			host = "localhost",
			user = admin,
			password = adminPassword
			)
	cursor = db.cursor()
	command = "CREATE USER IF NOT EXISTS '"+username+"'@'localhost' IDENTIFIED BY '"+password+"'"
	cursor.execute(command)
	priv = "GRANT ALL PRIVILEGES "+database+". * TO '"+username+"'@'localhost'"
	cursor.execute(priv)
	flush = "FLUSH PRIVILEGES"
	cursor.execute(flush)
	db.commit()
	cursor.close()
	return 1

def create_ipfs_tables(username,password,db):
	db = mysql.connector.connect(
			host = "localhost",
			user = username,
			password = password,
			database = db
			)
	cursor = db.cursor()
	tables = [["applications","ipfs text,devID text,appID text,version double,downloads int"],
		["assets","ipfs text,devID text,appID text,version double,downloads int"],
		["audio","ipfs text,author text,title text,post text,img text,date timestamp,ogg text,curation text,type text,genre text,tags text,duration text"],
		["images","ipfs text,source text,originated text,type text ,version double"],
		["video","ipfs text,author text,title text,post text,img text,date double,webm text,curation text,type text,genre text,tags text,duration text"]
		]
	for tab in tables: 
		command = "CREATE TABLE IF NOT EXISTS" + tab[0] +"("+tab[1]+")"
		cursor.execute(command)
		db.commit()

	cursor.close()
	return 1

def create_openseed_tables(username,password,db):
	db = mysql.connector.connect(
			host = "localhost",
			user = username,
			password = password,
			database = db
			)
	cursor = db.cursor()
	tables = [["applications","appNum int AUTO_INCREMENT,devID text,appID text,publicID text,appName text, date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"],
		["app_data_priv","count int AUTO_INCREMENT, devID text, appID text, data text , date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"],
		["app_data_pub","count int AUTO_INCREMENT, devID text, appID text, data text, date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"],
		["chat","id int AUTO_INCREMENT , room text , title text , attendees text, record blob, date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, speaker text"]
		["connections","connect_id int AUTO_INCREMENT, userid1 text, userid2 text , response int,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["developers","devnum int AUTO_INCREMENT,devID text,publicID text,devName text,contactName text,contactEmail text,steem text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["ft_ledger","count int AUTO_INCREMENT,token_id text,creator_id text,hash text,owner_id text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["history","count int AUTO_INCREMENT,account text,appid text,type tinytext,data text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["location","count int AUTO_INCREMENT,userID text,appPubID text,location text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["logins","login_index int AUTO_INCREMENT,username text,appid text,lastseen timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,data text"]
		["nft_ledger","count int AUTO_INCREMENT,token_id text,creator_id text,hash text,owner_id text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["nft_library","count int AUTO_INCREMENT,token_id text,creator_id text,version int,type int,preview text,asset text,unique_data text,description blob,upgradable tinyint,license int,license_file text,hash text,number int,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["nft_schema","count int AUTO_INCREMENT,token_base_id text,creator_id text,version int,type int,preview text,asset text,unique_data text,description blob,upgradable tinyint,license int,license_file text","total_available int,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["onetime","codeNum int AUTO_INCREMENT,type int,code text,registered text,validusers text,room text,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["profiles","id text,data1 text,data2 text,data3 text,data4 text,data5 text,type varchar,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		["users","userNum int AUTO_INCREMENT, userid text,userPub text,username text, email text, steem text, creationdate timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,verified text"]
		["temp_data","temp_index int AUTO_INCREMENT,devID text,appID text,data mediumtext,date timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		]
	for tab in tables: 
		command = "CREATE TABLE IF NOT EXISTS" + tab[0] +"("+tab[1]+")"
		cursor.execute(command)
		cursor.commit()

	db.commit()
	cursor.close()
	return 1

def create_openseed_sync_tables(username,password,db):
	db = mysql.connector.connect(
			host = "localhost",
			user = username,
			password = password,
			database = db
			)
	cursor = db.cursor()
	tables = [["servers","count int AUTO_INCREMENT,seed text,account text,address text,updated timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,rank int,priority int"]
		  ["currentUsers","count int AUTO_INCREMENT,token text,account text,updated timestamp CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"]
		]
	for tab in tables: 
		command = "CREATE TABLE IF NOT EXISTS" + tab[0] +"("+tab[1]+")"
		cursor.execute(command)
		cursor.commit()

	db.commit()
	cursor.close()
	return 1


if len(sys.argv) > 1 and sys.argv[1] == "new":
	create_node()
	
