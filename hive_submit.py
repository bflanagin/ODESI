#!/usr/bin/python
import sys
import mysql.connector
import hashlib
from hive import hive
from hive import wallet
sys.path.append("..")
import openseed_setup as Settings

settings = Settings.get_settings()
thenodes = ['anyx.io','api.hive.house','hive.anyx.io','hived.minnowsupportproject.org','hived.privex.io']
h = hive.Hive(nodes=thenodes)
w = wallet.Wallet
fix_thy_self = wallet.Wallet()

w.unlock(fix_thy_self,user_passphrase=settings["passphrase"])

postingKey = w.getPostingKeyForAccount(fix_thy_self,settings["hiveaccount"])
h.keys = postingKey
who = settings["hiveaccount"]

def memo(username,hivename,code):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = settings["dbuser"],
	password = settings["dbpassword"],
	database = "openseed"
	)
	service_type = "hive"
	codesearch = openseed.cursor()
	link = "Thank you for registering your hive account on OpenSeed. Please copy and paste this link : http://142.93.27.131:8675/account.py?act=verify&hivename="+str(hivename)+"&username="+str(username)+"&onetime="+str(code)+" into your address bar to finish the process"
	tamount = 0.001
	h.commit.transfer(to=hivename,amount=tamount,asset='hive',memo=link,account=who)
	update = "UPDATE `onetime` SET `sent` = TRUE WHERE `type` = '"+service_type+"' AND `user` = '"+username+"'"
	codesearch.execute(update)
	openseed.commit()
	codesearch.close()
	openseed.close()

def create_json(devID,appID,user,theid,data):
	
	post = '{"appId":"'+str(appId)+'","devId":"'+str(devId)+'","userId":"'+str(userId)+'","score":"'+str(score)+'"}'
	h.commit.custom_json(id=theid, json=post)

def create_post(devID,appID,publicID,title,data):
	
	return

def like_post(name,post):
	upvote_pct = 30
	already_voted = -1
	# Gets votes on the post
	result = h.get_active_votes(name, post)
	if result:
		# We run through the votes to make sure we haven't already voted on this post
		for vote in result:
			if vote['voter'] == who:
				already_voted = 1
				break
			else:
				already_voted = 0

		if already_voted == 0:
			identifier = ('@'+name+'/'+post)
			print("voting on ",identifier)	
			h.commit.vote(identifier, float(upvote_pct), who)
			post_reply(name,post)
		else:
			print("Voted already")


def openseed_post_reply(author,post,body):
	reply_identifier = '/'.join([author,post])
	print(reply_identifier)
	h.commit.post(title='', body=body, author=who, permlink='',reply_identifier=reply_identifier) 
	print("Adding reply")
	return

def openseed_post(author,post,body,title,json):
	h.commit.post(title=title, body=body, author=who, permlink='') 
	print("adding post")
	return

def leaderboard(devID,appID,user,data,hive,postingkey):
	h.wallet.addPrivateKey(postingkey)
	h.keys = postingkey
	update = '{"devID":"'+str(devID)+'","appID":"'+str(appID)+'","user":"'+str(user)+'","data":"'+str(data)+'"}'
	tamount = 0.001
	h.commit.transfer(to="openseed",amount=tamount,asset='hive',memo=update,account=hive)

def payment(hiveaccount,to_account,amount,data,postingkey):
	if w.getActiveKeyForAccount(hiveaccount):
		h.keys = w.getActiveKeyForAccount(hiveaccount)
	else:
		w.addPrivateKey(postingkey)
		h.keys = postingkey

	receipt = str(data)+' via Thicket'
	asset = 'HIVE'
	if amount.split(",")[1].split("]")[0] == 1:
		asset = 'HBD'
	payout = amount.split(",")[0].split("[")[1]
	h.commit.transfer(to=to_account,amount=float(payout),asset=asset,memo=receipt,account=hiveaccount)
	return('{"sent":"'+to_account+'"}')

def set_allow(hiveaccount, hiveapp):

	return

def remove_allow(hiveaccount, hiveapp):

	return

def flush_account(hiveaccount):
	w.removeAccount(hiveaccount)
	return('{"removed":"'+hiveaccount+'"}')

