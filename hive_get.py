#!/usr/bin/python

import subprocess
import sys
import time
sys.path.append("..")
import mysql.connector
import json
from hive import hive
import openseed_music as Music
import hive_submit as Submit
import openseed_ipfs as IPFS
import openseed_setup as Settings
import openseed_account as Account

settings = Settings.get_settings()
thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
s = hive.Hive(nodes=thenodes)

songtype = "NA"
genre = "NA"
artist = "NA"
permlink = "NA"
ipfs = "NA"
img = "NA"
songtags = "NA"
duration = "0.00"
title = "New Song"


def get_post(author,permlink) :
 post = s.get_content(author,permlink)
 return post["body"]

def get_account(account):
 profile = '{"profile":"Not found"}'
 full_account = s.get_account(account)
 if full_account:
  profile = full_account["json_metadata"]
 return(profile)

def get_full_account(account):
 profile = '{"profile":"Not found"}'
 full_account = s.get_account(account)
 if full_account:
  profile = json.dumps(full_account)
 return(profile)

def get_connections(account):
 connection = []
 follows = []
 watching = []
 followers = s.get_followers(account,0,"",1000)
 following = s.get_following(account,0,"",1000)
 if str(followers).find("error") == -1:
 	for flwrs in followers:
  		follows.append(flwrs["follower"])
 if str(following).find("error") == -1:
 	for flws in following:
  		watching.append(flws["following"])

 for er in follows:
  for ing in watching:
   if er == ing:
    connection.append('connection:'+er)

 return(json.dumps(connection))


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
 print(author,limit)
 local = local_search(author)
 activity = s.get_account_history(author,index_from = -1,limit = limit)
 for post_info in activity :
  if post_info != None:
   if post_info[1]["op"][0] == "comment" and post_info[1]['op'][1]['author'] == author:
    permlink = post_info[1]['op'][1]['permlink']
    title = post_info[1]['op'][1]['title']
    if str(post_info[1]["op"][1].keys()).find("json_metadata") != -1:
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
         print("found audio "+title)
 return(local)

def search_history(user,limit):
 openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
 mysearch = openseed.cursor()
 search = "SELECT userId FROM `users` WHERE steem = %s"
 mysearch.execute(search,(user,))
 result = mysearch.fetchall()

 activity = s.get_account_history(user,index_from = -1,limit = limit)
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
    	Account.update_history(str(result[0][0].replace('\x00',"")),9,"steem",str(data))
    break


 mysearch.close()
 openseed.close()

 return


def pin_and_record(ipfs,author,title,post,img,songtype,genre,songtags,duration):
 openseed = mysql.connector.connect(
	host = "localhost",
	user = settings["ipfsuser"],
	password = settings["ipfspassword"],
	database = "ipfsstore"
	)
 mysearch = openseed.cursor()
 search = "SELECT title,duration,genre,date,curation FROM `audio` WHERE `ipfs`='"+str(ipfs)+"'"
 mysearch.execute(search)
 song = mysearch.fetchall()
 result = len(song)
 sql = ""
 values = ""
 
 if result > 1:
  delete = openseed.cursor()
  sql = "DELETE FROM `audio` WHERE ipfs = %s AND date NOT LIKE %s"
  val = (str(ipfs),str(song[0][3]))
  delete.execute(sql,val)
  delete.close()
  openseed.commit()
 if result == None or result == 0:
  mycursor = openseed.cursor() 
  print(title)
  time.sleep(3)
  Submit.like_post(author,post) 
  sql = "INSERT INTO `audio` (`ipfs`,`author`,`title`,`post`,`img`,`type`,`genre`,`tags`,`duration`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  values = (str(ipfs),str(author),str(title),str(post),str(img),str(songtype),str(genre),str(songtags),str(duration))
  mycursor.execute(sql,values)
  openseed.commit()
  subprocess.Popen(["/usr/bin/ipfs","pin","add",str(img)])
  ipfs = subprocess.Popen(["/usr/bin/ipfs","pin","add",str(ipfs)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  #ipfs.wait()
  #stdout, stderr = ipfs.communicate()
  mycursor.close()
 elif(result == 1):
  if song[0][2] == "NULL" or song[0][2] == "" or song[0][2] == None or song[0][2] == "null":
   updatecursor = openseed.cursor()
   sql = "UPDATE audio SET type = %s, genre = %s, tags = %s, duration = %s WHERE ipfs = %s"
   values = (str(songtype),str(genre),str(songtags),str(duration),str(ipfs))
   updatecursor.execute(sql,values)
   openseed.commit()

 openseed.close()

