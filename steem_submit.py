#!/usr/bin/python

import mysql.connector
import hashlib
from steem import Steem

s = Steem()
who = ''
s.wallet.unlock(user_passphrase='')
postingKey = s.wallet.getPostingKeyForAccount(who)
s.keys = postingKey

def memo(username,steemname,code):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
	service_type = "steem"
	codesearch = openseed.cursor()
	link = "Thank you for registering your steem account on OpenSeed. Please copy and paste this link : http://142.93.27.131:8675/account.py?act=verify&steemname="+str(steemname)+"&username="+str(username)+"&onetime="+str(code)+" into your address bar to finish the process"
	tamount = 0.001
	s.commit.transfer(to=steemname,amount=tamount,asset='STEEM',memo=link,account=who)
	update = "UPDATE `onetime` SET `sent` = TRUE WHERE `type` = '"+service_type+"' AND `user` = '"+username+"'"
	codesearch.execute(update)
	openseed.commit()
	codesearch.close()
	openseed.close()

def create_json(devID,appID,user,theid,data):
	
	post = '{"appId":"'+str(appId)+'","devId":"'+str(devId)+'","userId":"'+str(userId)+'","score":"'+str(score)+'"}'
	s.commit.custom_json(id=theid, json=post)

#def create_post(devID,appID,publicID,title,data):



def leaderboard(devID,appID,user,data,steem,postingkey):
	s.wallet.addPrivateKey(postingkey)
	s.keys = postingkey
	update = '{"devID":"'+str(devID)+'","appID":"'+str(appID)+'","user":"'+str(user)+'","data":"'+str(data)+'"}'
	tamount = 0.001
	s.commit.transfer(to="openseed",amount=tamount,asset='STEEM',memo=update,account=steem)

def payment(steemaccount,to_account,amount,data,postingkey):
	if s.wallet.getActiveKeyForAccount(steemaccount):
		s.keys = s.wallet.getActiveKeyForAccount(steemaccount)
	else:
		s.wallet.addPrivateKey(postingkey)
		s.keys = postingkey

	receipt = str(data)+' via Thicket'
	asset = 'STEEM'
	if amount.split(",")[1].split("]")[0] == 1:
		asset = 'SBD'
	payout = amount.split(",")[0].split("[")[1]
	s.commit.transfer(to=to_account,amount=float(payout),asset=asset,memo=receipt,account=steemaccount)
	return('{"sent":"'+to_account+'"}')

def save_map(devID,appID,user,data):
	#Will need to add various checks before data is sent
	create_json(devID,appID,user,"map",data)

def save_game(devID,appID,user,data):
	#Will need to add various checks before data is sent
	create_json(devID,appID,user,"map",data)

def edit_map(devID,appID,user,post,data):
	#Will need to add various checks before data is sent
	create_json(devID,appID,user,"map",data)

def edit_game(devID,appID,user,post,data):
	#Will need to add various checks before data is sent
	create_json(devID,appID,user,"map",data)

def flush_account(steemaccount):
	s.wallet.removeAccount(steemaccount)
	return('{"removed":"'+steemaccount+'"}')

