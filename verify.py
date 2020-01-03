#!/usr/bin/python
import cgi
import cgitb
import sys
import mysql.connector
import hashlib

from steem import Steem

import openseed_setup as Settings

settings = Settings.get_settings()

s = Steem()
s.wallet.unlock(user_passphrase=settings["passphrase"])
postingKey = s.wallet.getPostingKeyForAccount(settings["steemaccount"])
s.keys = postingKey
username = ''
code = ''

def get_onetime(service_type):

	openseed = mysql.connector.connect(
	host = "localhost",
	user = settings["dbuser"],
	password = settings["dbpassword"],
	database = "openseed"
	)
	codesearch = openseed.cursor()
	search = "SELECT * FROM `onetime` WHERE `type` = '"+service_type+"' AND `sent` = FALSE"
	codesearch.execute(search)
	result = codesearch.fetchall()
	for row in result:
		username=str(row[1]).split("'")[1]
		code = str(row[2]).split("'")[1]
		link = "Thank you for registering your steem account on OpenSeed. Please copy and paste this link : http://142.93.27.131:8675/account.py?act=verify&username="+str(username+"&onetime="+str(code))+" into your address bar to finish the process"
		tamount = 0.001
		s.commit.transfer(to=username,amount=tamount,asset='STEEM',memo=link,account=who)
		update = "UPDATE `onetime` SET `sent` = TRUE WHERE `type` = '"+service_type+"' AND `user` = '"+username+"'"
		codesearch.execute(update)
		openseed.commit()
		codesearch.close()
		openseed.close()
	return

get_onetime('steem')

