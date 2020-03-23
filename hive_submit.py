#!/usr/bin/python
import sys
import mysql.connector
import hashlib
from steem import Steem
sys.path.append("..")
import openseed_setup as Settings

settings = Settings.get_settings()
thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
s = Steem()

s.wallet.unlock(user_passphrase=settings["passphrase"])
postingKey = s.wallet.getPostingKeyForAccount(settings["steemaccount"])
s.keys = postingKey
who = settings["steemaccount"]

def memo(username,steemname,code):
	openseed = mysql.connector.connect(
	host = "localhost",
	user = settings["dbuser"],
	password = settings["dbpassword"],
	database = "openseed"
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

def create_post(devID,appID,publicID,title,data):
	
	return

def like_post(name,post):
	upvote_pct = 30
	already_voted = -1
	# Gets votes on the post
	result = s.get_active_votes(name, post)
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
			s.commit.vote(identifier, float(upvote_pct), who)
			#post_reply(name,post)
		else:
			print("Voted already")


def openseed_post_reply(author,post,body):
	reply_identifier = '/'.join([author,post])
	print(reply_identifier)
	s.commit.post(title='', body=body, author=who, permlink='',reply_identifier=reply_identifier) 
	print("Adding reply")
	return

def openseed_post(author,post,body,title,json):
	s.commit.post(title=title, body=body, author=who, permlink='') 
	print("adding post")
	return

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

