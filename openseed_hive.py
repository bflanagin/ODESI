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


#!/usr/bin/python

import subprocess
import sys
import time
sys.path.append("..")
import mysql.connector
import json
from hive import hive
import openseed_music as Music
import openseed_ipfs as IPFS
import openseed_setup as Settings
import openseed_account as Account

settings = Settings.get_settings()
thenodes = ['anyx.io','api.hive.house','hive.anyx.io','hived.minnowsupportproject.org','hived.privex.io']
h = hive.Hive(nodes=thenodes)

songtype = "NA"
genre = "NA"
artist = "NA"
permlink = "NA"
ipfs = "NA"
img = "NA"
songtags = "NA"
duration = "0.00"
title = "New Song"


##############################
#
# Retrevial Functions
#
##############################



def get_post(author,permlink) :
	post = h.get_content(author,permlink)
	return post["body"]

def get_account(account):
	profile = '{"profile":"Not found"}'
	full_account = h.get_account(account)
	if full_account:
		profile = full_account["json_metadata"]
	return(profile)

def get_full_account(account):
	profile = '{"profile":"Not found"}'
	full_account = h.get_account(account)
	if full_account:
		profile = json.dumps(full_account)
	return(profile)

def get_connections(account):
	connections = []
	follows = []
	watching = []
	followers = h.get_followers(account,0,"",1000)
	following = h.get_following(account,0,"",1000)
	if str(followers).find("error") == -1:
		for flwrs in followers:
			follows.append(flwrs["follower"])
	if str(following).find("error") == -1:
		for flws in following:
			watching.append(flws["following"])

	for er in follows:
		for ing in watching:
			if er == ing:
				hiveaccount = json.loads(get_account(er))
				if "profile" in hiveaccount and hiveaccount["profile"] != "Not found":
					theName = er
					theAbout = ""
					theProfileImg = ""
					theBannerImg = ""
					
					if "name" in hiveaccount["profile"]:
						theName = hiveaccount["profile"]["name"]
					if "about" in hiveaccount["profile"]:
						theAbout = hiveaccount["profile"]["about"]
					if "profile_image" in hiveaccount["profile"]:
						theProfileImg = hiveaccount["profile"]["profile_image"]
					if "cover_image" in hiveaccount["profile"]:
						theBannerImg = hiveaccount["profile"]["cover_image"]

					data1 = '{"name":"'+theName+'","email":"","phone":"","profession":"","company":""}'
					data2 = '{"about":"","profile_img":"'+theProfileImg+'","banner":"'+theBannerImg+'"}'
					blank_p = '"profile":{"openseed":'+data1+',"extended":{},"appdata":{},"misc":{},"imports":{}}'
					connections.append('{"username":"'+er+'","linked":"1",'+blank_p+'}')


	return(connections)


## Music specific functions (should be moved at some point ##

def local_search(author):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	mysearch = openseed.cursor()
	search = "SELECT * FROM `audio` WHERE `author`='"+str(author)+"'"
	mysearch.execute(search)
	result = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	if result == 0:
		return("{New Artist}")
	else:
		return (Music.get_artist_tracks(author))


def search_music(author,limit) :
	#print(author,limit)
	local = local_search(author)
	activity = h.get_account_history(author,index_from = -1,limit = limit)
	for post_info in activity :
		if post_info != None:
			if post_info[1]["op"][0] == "comment" and post_info[1]['op'][1]['author'] == author:
				permlink = post_info[1]['op'][1]['permlink']
				title = post_info[1]['op'][1]['title']
				if str(post_info[1]["op"][1].keys()).find("json_metadata") != -1:
					if len(post_info[1]["op"][1]["json_metadata"]) > 5:
						metadata = json.loads(post_info[1]["op"][1]["json_metadata"])
						if metadata != '{"app":"threespeak/1.0"}' and metadata != '' and str(metadata.keys()).find("tags") != -1:
							tags = metadata["tags"]
							if tags != None:
								if str(tags).find("dsound") != -1:
									if str(metadata.keys()).find("audio") != -1:
										songtype = metadata["audio"]["type"]
										songtags = tags
										duration = metadata["audio"]["duration"]
										ipfs = metadata["audio"]["files"]["sound"]
										artist = author
										img = metadata["audio"]["files"]["cover"]
										genre = metadata["audio"]["genre"]
										IPFS.pin_and_record(ipfs,artist,title,permlink,img,songtype,genre,songtags,duration)
	return(local)

def search_history(user,limit):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT userId FROM `users` WHERE hive = %s"
	mysearch.execute(search,(user,))
	result = mysearch.fetchall()

	activity = h.get_account_history(user,index_from = -1,limit = limit)
	tags = ""
	for post_info in activity :
		if post_info != None:
			if post_info[1]["op"][0] == "comment" and post_info[1]['op'][1]['author'] == user:
				permlink = post_info[1]['op'][1]['permlink']
				title = post_info[1]['op'][1]['title']
				if str(post_info[1]["op"][1].keys()).find("json_metadata") != -1:
					if len(post_info[1]["op"][1]["json_metadata"]) > 4:
						metadata = json.loads(post_info[1]["op"][1]["json_metadata"])
						if metadata != '' and str(metadata.keys()).find("tags") != -1:
							tags = metadata["tags"]
				if len(title) > 2:
					data = '{"post":{"title":"'+title+'","permlink":"'+permlink+'","tags":"'+str(tags)+'"}}'
					Account.update_history(str(result[0][0].replace('\x00',"")),9,"hive",str(data))
				break


	mysearch.close()
	openseed.close()

	return


######################################
#
# Submission functions. 
#
######################################

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

def payment(hiveaccount,to_account,amount,data,postingkey):
	if w.getActiveKeyForAccount(hiveaccount):
		h.keys = w.getActiveKeyForAccount(hiveaccount)
	else:
		w.addPrivateKey(postingkey)
		h.keys = postingkey

	receipt = str(data)+' via OpenSeed'
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
			else:
				new = json.loads(Account.external_user(acc,postkey,"hive"))
				Account.create_default_profile(new["token"],new["username"],"")
				update_account(new["username"],new["username"])

def import_profile(account,hiveaccount):

	openseed = json.loads(

	hive = json.loads(get_account(hiveaccount))
	
	print(hive)

	return			
					

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

def set_delegation(acc, hiveapp, privatekey=""):
	postingKey = w.getPostingKeyForAccount(fix_thy_self,acc)
	h.keys = postingKey
	who = acc
	h.commit.allow(hiveapp,permission="posting",account=acc)
	
	return '{delegation:{"account":"'+acc+'","rights":"posting","to":"'+hiveapp+'"}'

def remove_delegation(acc, hiveapp, privatekey=""):
	postingKey = w.getPostingKeyForAccount(fix_thy_self,acc)
	h.keys = postingKey
	who = acc
	h.commit.disallow(hiveapp,permission="posting",account=acc)
	
	return '{delegation:{"account":"'+acc+'","rights":"removed","to":"'+hiveapp+'"}'

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

