#!/usr/bin/python

import subprocess
import sys
sys.path.append("..")
import mysql.connector
import json
from steem import Steem
import openseed_music as Music

s = Steem()

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

 for flwrs in followers:
  follows.append(flwrs["follower"])
 for flws in following:
  watching.append(flws["following"])
 for er in follows:
  for ing in watching:
   if er == ing:
    connection.append('connection:'+er)

 return(json.dumps(connection))


## Music specific functions (should be moved at some point ##

def local_search(author):
 mydb = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
 mysearch = mydb.cursor()
 search = "SELECT * FROM `audio` WHERE `author`='"+str(author)+"'"
 mysearch.execute(search)
 result = len(mysearch.fetchall())
 mysearch.close()
 mydb.close()
 if result == 0:
  return("{New Artist}")
 else:
  return (Music.get_artist_tracks(author))


def search_artist(author,limit) :
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
        pin_and_record(ipfs,artist,title,permlink,img,songtype,genre,songtags,duration)
 return(local)


def pin_and_record(ipfs,author,title,post,img,songtype,genre,songtags,duration):
 mydb = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
 mysearch = mydb.cursor()
 search = "SELECT title,duration FROM `audio` WHERE `ipfs`='"+str(ipfs)+"'"
 mysearch.execute(search)
 song = mysearch.fetchall()
 result = len(song)
 sql = ""
 values = ""
 if result != 1:
  mycursor = mydb.cursor()  
  sql = "INSERT INTO `audio` (`ipfs`,`author`,`title`,`post`,`img`,`type`,`genre`,`tags`,`duration`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  values = (str(ipfs),str(author),str(title),str(post),str(img),str(songtype),str(genre),str(songtags),str(duration))
  mycursor.execute(sql,values)
  mydb.commit()
  subprocess.Popen(["/usr/bin/ipfs","pin","add",str(img)])
  ipfs = subprocess.Popen(["/usr/bin/ipfs","pin","add",str(ipfs)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  #ipfs.wait()
  #stdout, stderr = ipfs.communicate()
  mycursor.close()
  #oggify_and_share(str(stdout).split(" ")[1])
 else:
  if len(song[0]) == 1:
   updatecursor = mydb.cursor()
   sql = "UPDATE audio SET type = %s, genre = %s, tags = %s, duration = %s WHERE ipfs = %s"
   values = (str(songtype),str(genre),str(songtags),str(duration),str(ipfs))
   updatecursor.execute(sql,values)
   mydb.commit()

 mydb.close()


def oggify_and_share(thehash):
 mydb = mysql.connector.connect(
	host = "localhost",
	user = "",
	password = "",
	database = ""
	)
 mysearch = mydb.cursor()
 search = "SELECT ipfs,img FROM `audio` WHERE ipfs ='"+thehash+"'"
 mysearch.execute(search)
 result = mysearch.fetchall()
 process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 process.wait()
 stdout, stderr = process.communicate()
 stored = str(stdout)
 if str(stderr) == "b''":
  reformat = subprocess.Popen(['ffmpeg', '-n','-i', 'http://142.93.27.131:8080/ipfs/'+thehash, '-vn', '-c:a', 'libvorbis', '-q:a', '4', '/mnt/volume_sfo2_01/openseed/music/'+str(r[0])+'.ogg'])
  reformat.wait()
  add_to_ipfs = subprocess.Popen(['ipfs', 'add' , '/mnt/volume_sfo2_01/openseed/music/'+thehash+'.ogg'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  add_to_ipfs.wait()
  stdout, stderr = add_to_ipfs.communicate()
  updatesql = mydb.cursor()
  sql = "UPDATE audio SET ogg = '"+str(stdout).split(" ")[1]+"' WHERE ipfs ='"+thehash+"'"
  updatesql.execute(sql)
  mydb.commit()
  mydb.close()
