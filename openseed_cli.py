#!/usr/bin/python

import sys
sys.path.append("..")
import mysql.connector
import openseed_account as Account
import hive_get as Get
import hive_submit as Submit
import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_connections as Connections
import openseed_chat as Chat
import onetime as OneTime
import openseed_token as Tokens

import openseed_setup as Settings

settings = Settings.get_settings()

import json

if len(sys.argv) > 1:	
	if sys.argv[1] == "new":
		
		if sys.argv[2] == "creator":
			print("Creating new Creator account\n")
			devName = input("Creator Name: ")
			contactName = input("Main contact name: ")
			contactEmail = input(contactName+"'s email address: ")
			steem = input("Steem account for the creator account: ") 
			Account.create_developer(devName,contactName,contactEmail,steem)
			
		elif sys.argv[2] == "app":
			print("Creating new App account\n")
			devID = input("Developer Public ID: ")
			appName = input("Application Name: ")
			result = Account.create_app(devID,appName)
			print(result)

		elif sys.argv[2] == "FT":
			devID = input("Public Developer ID: ")
			appID = input("Public Application ID(optional): ")
			total = input("Total supply: ")
			precision = input("Precision (defaults to two decimals): ")
			Tokens.create_ft(devID,appID,"","",total,precision)

		elif sys.argv[2] == "NFT":
			print("Creating NFT ledger\n")
			devID = input("Public Developer ID: ")
			appID = input("Public Application ID(optional): ")
			total = input("Total supply: ")
			Tokens.create_nft(devID,appID,total,precision)

	

