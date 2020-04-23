#!/usr/bin/python
import sys
import mysql.connector
import hashlib
import json
from hive import hive
from hive import wallet
import openseed_account as Account
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
			#post_reply(name,post)
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

def check_account(account,postkey):
	hiveaccount = w.getAccountFromPrivateKey(fix_thy_self,postkey)
	if account == hiveaccount:
		return 1
	else:
		return 0
	
def store_key(account,key):
	w.addPrivateKey(fix_thy_self,key)
	return 1 
	
def import_account(account,masterpass):

	return

def openseed_interconnect(openseed,acc,postkey,storekeys):

	if check_account(acc,postkey) == 1:
		exists = Account.check_db(acc,"users")
		if exists !=0:
			print("user exists")
			print("checking if hive account is connected to an openseed account")
			verifing = json.loads(check_verified(openseed,acc))
			if verifing["openseed"] == 1 and verifing["openseed"] == verifing["hive"]:
				return '{"interconnect":"connected","account_auth":"openseed","keystored":'+str(storekeys)+'}'
			elif verifing["openseed"] == 0 and verifing["hive"] == 1:
				return '{"interconnect":"Hive account in use","account_auth":"error","keystored":false}'
			elif verifing["openseed"] == 1 and verifing["hive"] == 0:
				if update_account(openseed,acc) == 1:
					if store_key(acc,postkey) == 1:
						set_delegation(acc,"openseed")
					if storekeys == False:
						flush_account(acc)
					return '{"interconnect":"connected","account_auth":"openseed","keystored":'+str(storekeys)+'}'
					

def check_verified(openseed,hive):
	
	db = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mycursor = db.cursor()
	
	find_openseed = "SELECT username,hive FROM `users` WHERE username = %s"
	openseed_val = (openseed,)
	mycursor.execute(find_openseed,openseed_val)
	
	openseed_result = mycursor.fetchall()
	find_hive = "SELECT username,hive FROM `users` WHERE hive = %s"
	hive_val = (hive,)
	mycursor.execute(find_hive,hive_val)
	hive_result = mycursor.fetchall()	
	db.close()
	
	return '{"openseed":'+str(len(openseed_result))+',"hive":'+str(len(hive_result))+'}'

def find_keys_by_accountname(account):

	return

def set_delegation(acc, hiveapp):
	postingKey = w.getPostingKeyForAccount(fix_thy_self,acc)
	h.keys = postingKey
	who = acc
	h.commit.allow("openseed",permission="posting",account=acc)
	
	return 1

def remove_delegation(acc, hiveapp):
	postingKey = w.getPostingKeyForAccount(fix_thy_self,acc)
	h.keys = postingKey
	who = acc
	h.commit.disallow(hiveapp,permission="posting",account=acc)
	
	return 1

def flush_account(hiveaccount):
	w.removeAccount(fix_thy_self,hiveaccount)
	return('{"removed":"'+hiveaccount+'"}')
	
def update_account(openseed,account):
	db = mysql.connector.connect(
	host = "localhost",
	user = settings["dbuser"],
	password = settings["dbpassword"],
	database = "openseed"
	)
	
	update = db.cursor()
	update_string = "UPDATE `users` SET hive = %s WHERE username = %s"
	val = (account,openseed)
	update.execute(update_string,val)
	db.commit()
	update.close()
	db.close()
	return 1

