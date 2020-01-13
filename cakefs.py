#!/usr/bin/python

import subprocess
import sys
import mysql.connector
import json
import datetime
import random
import string
import steembase
import requests
import datetime

from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
from steem.blog import Blog

s = Steem()

import openseed_setup as Settings

settings = Settings.get_settings()

openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
def check_pins(type,num):
 mysearch = openseed.cursor()
 search = "SELECT ipfs,img FROM `"+str(type)+"` WHERE 1 ORDER BY date DESC"
 mysearch.execute(search)
 result = mysearch.fetchall()

 filecount = 0
 imagecount = 0
 print("Main file")
 for r in result:
  
   if filecount <= int(num):
    process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', str(r[0])], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    stored = str(stdout)
    if str(stderr) != "b''":
     print(str(r[0])+" Not pinned")
     filecount += 1
     subprocess.Popen(["ipfs","pin","add",str(r[0])])
 print("Img file")
 for r in result:
  
  if imagecount <= int(num):
    process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', str(r[1])], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    stored = str(stdout)
    if str(stderr) != "b''":
      print(str(r[1])+" Not pinned")
      imagecount +=1
      subprocess.Popen(["ipfs","pin","add",str(r[1])])

def pin_and_record(ipfs,author,title,post,img,type):
 mysearch = openseed.cursor()
 search = "SELECT * FROM `"+str(type)+"` WHERE `ipfs`='"+str(ipfs)+"'"
 mysearch.execute(search)
 result = len(mysearch.fetchall())
 if result != 1:
  mycursor = openseed.cursor()
  sql = "INSERT INTO `"+str(type)+"` (`ipfs`,`author`,`title`,`post`,`img`,`curation`) VALUES (%s,%s,%s,%s,%s,%s)"
  values = (str(ipfs),str(author),str(title),str(post),str(img),"helpiecake")
  mycursor.execute(sql,values)
  openseed.commit()
  subprocess.Popen(["/usr/bin/ipfs","pin","add",str(ipfs)])
  subprocess.Popen(["/usr/bin/ipfs","pin","add",str(img)])

def scan_post(name,post):
 content = s.get_content(name,post)
 if content['body'].find('/ipfs/') != -1:
  if content['body'].find('dsound.audio/ipfs/') != -1:
   title = content['title']
   links = content['body'].split("<a href=")
   image = content['body'].split("<img src=")[1].split("ipfs/")[1].split('"')[0]
   for l in links:
    if l.find("img") == -1:
     if l.find("/ipfs") != -1:
      ipfs = l.split('dsound.audio/ipfs/')[1].split('"')[0]
      pin_and_record(ipfs,name,title,post,image,"audio")
      print("Pinning "+name)

def dtube_ipfs(url):
 r = requests.get(url)
 page = r.text
 #print (page.find("/ipfs/"))
 return "boop: "+url

def oggify_and_share(type):
 mysearch = openseed.cursor()
 search = "SELECT ipfs,img FROM `"+str(type)+"` WHERE ogg IS NULL OR ogg NOT LIKE '_%'"
 mysearch.execute(search)
 result = mysearch.fetchall()
 print("Main file")
 for r in result:
   process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', str(r[0])], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   process.wait()
   stdout, stderr = process.communicate()
   stored = str(stdout)
   if str(stderr) == "b''":
     reformat = subprocess.Popen(['ffmpeg', '-n','-i', 'http://142.93.27.131:8080/ipfs/'+str(r[0]), '-vn', '-c:a', 'libvorbis', '-q:a', '4', '/mnt/volume_sfo2_01/openseed/music/'+str(r[0])+'.ogg'])
     reformat.wait()
     add_to_ipfs = subprocess.Popen(['ipfs', 'add' , '/mnt/volume_sfo2_01/openseed/music/'+str(r[0])+'.ogg'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
     add_to_ipfs.wait()
     stdout, stderr = add_to_ipfs.communicate()
     updatesql = openseed.cursor()
     sql = "UPDATE audio SET ogg = '"+str(stdout).split(" ")[1]+"' WHERE ipfs ='"+str(r[0])+"'"
     updatesql.execute(sql)
     openseed.commit()

def report_generator(type):
 report = open("audio_report.md" , "w")
 records = openseed.cursor()
 search = "SELECT * FROM `"+str(type)+"` WHERE 1"
 records.execute(search)
 result = records.fetchall()
 thedate = datetime.datetime.now()
 report.write("CakeFS 0.1 - "+str(thedate)+"\n")
 report.write("\n---\n")
 report.write("<p> CakeFS is a small script created to automate the collection and distribution of manually curated content. Each submission below was awarded cake via @helpiecake run by the @helpie community. As a part of the helpie team @bflanagin of @v-entertainment is hosting a IPFS server to help distribute and backup these files.</p>\n")
 report.write("\n---\n")
 report.write("# Audio Files\n")
 report.write("| Direct Link | Artist | Title | Date |\n|----|----|----|----|\n")
 for r in result:
   process = subprocess.Popen(['ipfs', 'pin', 'ls', '--type', 'recursive', str(r[0])], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   process.wait()
   stdout, stderr = process.communicate()
   if str(stderr) == "b''": 
     report.write("| <audio src='http://142.93.27.131:8080/ipfs/"+r[0]+"'>[Direct Link](http://142.93.27.131:8080/ipfs/"+r[0]+")</audio> |")
     report.write("["+r[1]+"](https://dsound.audio/#!/@"+r[1]+") | ["+r[2]+"](https://dsound.audio/#!/@"+r[1]+"/"+r[3]+") | "+str(r[5])+" |\n")
 report.close

if len(sys.argv) > 1 and sys.argv[1]:
  argument = sys.argv[1]
  if argument == "report":
    print("Report generating")
    report_generator("audio")
  elif argument == "check":
    print("Checking pins")
    check_pins("audio",sys.argv[2])
  elif argument == "oggify":
    print("Oggifying stored content")
    oggify_and_share("audio")
  else:
    print(argument)
else:
  helpie_cake = s.get_account_history('helpiecake', index_from=-1, limit = 10000)
  n = -1
  while n < 10000:
    if 'author' in helpie_cake[n][1]['op'][1]:
     if 'parent_author' in helpie_cake[n][1]['op'][1]:
       author = helpie_cake[n][1]['op'][1]['author']
       parent_author = helpie_cake[n][1]['op'][1]['parent_author']
       if author == 'helpiecake':
         if parent_author !='helpiecake':
           permlink = helpie_cake[n][1]['op'][1]['parent_permlink']
           scan_post(parent_author,permlink)
    n += 1
