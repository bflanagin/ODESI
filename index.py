#!/usr/bin/python
import cgi
import cgitb
import sys
import urllib
sys.path.append("..")
import openseed_account as Account
import openseed_setup as Settings
import openseed_utils as Utils
#import hive_get as Get
#import hive_submit as Submit
#import leaderboard as LeaderBoard
import openseed_seedgenerator as Seeds
import openseed_music as Music
import openseed_connections as Connections
import openseed_chat as Chat
import onetime as OneTime
import io

import json

form = cgi.FieldStorage()

dev_pub = form.getvalue("pub")
read_json = form.getvalue("msg")

get_image = form.getvalue("image")

if get_image != None:
	
	print("Content-type:text/html\r\n\r\n")
	
	get_size = form.getvalue("size")
	get_source_type = form.getvalue("source")
	if get_size != None and get_source_type != None:
		image = Utils.get_image(get_image,get_source_type,get_size)
		print("<html>")
		print("<body>")
		print("<img src=http://openseed.solutions:8080/ipfs/"+image+">")
		print("</body>")
		print("</html>")
		

else:
	print("Content-type:text/html\r\n\r\n")

if dev_pub == None:
	from_client = json.loads(read_json)
else:
	devID = Account.get_priv_from_pub(dev_pub)
	decrypted_message = Seeds.simp_decrypt(devID,read_json)
	from_client = json.loads(decrypted_message)
	
	
action = from_client["act"]

if Account.check_appID(from_client["appPub"],from_client["devPub"]):
	app = from_client["appPub"]
	dev = from_client["devPub"]
	
# Account Actions
 
	if action == "accountcheck":
		print(Account.accountCheck(from_client["username"],from_client["passphrase"]))
	if action == "steemcheck":
		print(Account.steem_Check(from_client["steemname"]))
	if action == "create":
		print(Account.create_user(from_client["username"],from_client["passphrase"],from_client["email"]))
	if action == "set_profile":
		print(Account.set_profile(from_client["token"],from_client["data1"],
			from_client["data2"],from_client["data3"],from_client["data4"],
			from_client["data5"],from_client["type"]))
	if action == "link":
		print(Account.steem_link(from_client["username"]))
	if action == "verify":
		print(Account.steem_verify(from_client["username"],from_client["onetime"]))
	if action == "account":
		print(Account.get_account(from_client["token"]))
	if action == "search":
		print(Account.openseed_search(from_client["username"]))
	if action == "gps":
		print(Account.gps_search(from_client["username"],from_client["cords"]))
	if action == "get_history":
		print(Account.get_history(from_client["account"],from_client["apprange"],from_client["count"]))
	if action == "update_history":
		print(Account.update_history(from_client["account"],from_client["type"],from_client["appPub"],from_client["data"]))

	if action == "web_auth":
		print()

#  Media Actions
			
	if action == "music":
		print(Music.get_curated_music(from_client["curator"]))
	if action == "music_json":
		print(Music.get_curated_music_json(from_client["curator"]))
	#if action == "post":
		#print(Get.get_post(from_client["author"],from_client["permlink"]))
	#if action == "artist_search":
		#print(Get.search_music(from_client["author"],10000))
	#if action == "getaccount":
		#print(Get.get_account(from_client["account"]))
	#if action == "getfullaccount":
		#print(Get.get_full_account(from_client["account"]))
	if action == "newaccounts":
		print(Music.get_new_artists())
	if action == "newtracks":
		print(Music.get_new_tracks())
	if action == "newtracks_json":
		print(Music.get_new_tracks_json())
	if action == "genres":
		print(Music.get_genres())
	if action == "genre":
		print(Music.get_genre_tracks(from_client["genre"]))
	if action == "genre_json":
		print(Music.get_genre_tracks_json(from_client["genre"],from_client["count"]))
	if action == "getArtistTracks":
		print(Music.get_artist_tracks_json(from_client["author"],from_client["count"]))
	if action == "getTracks":
		print(Music.get_tracks_json(from_client["start"],from_client["count"]))

# Chat Actions
 	
	if action == "get_status":
		print(Account.get_status(from_client["account"]))
	if action == "set_status":
		print(Account.set_status(from_client["appPub"],from_client["token"],from_client["status"]))

	if action == "get_conversations":
		print(Chat.get_conversations(from_client["token"]))

	if action == "create_chatroom":
		print(Chat.create_chatroom(from_client["token"],from_client["title"],from_client["attendees"],app))

	if action == "get_chat_history":
		print(Chat.get_chat_history(from_client["token"],from_client["room"],from_client["count"],from_client["last"]))	
	if action == "get_chat":
		print(Chat.get_chat(from_client["token"],from_client["room"],from_client["last"]))
	if action == "send_chat":
		print(Chat.send_chat(from_client["token"],from_client["room"],from_client["message"],app))
	
	if action == "check_chat":
		print(Chat.check_chat(from_client["token"],from_client["room"]))
	if action == "chat":
 		print(Chat.get_chat(from_client["token"],from_client["username"],from_client["chatroom"],from_client["data"]))

	if action == "find_room_by_attendees":
		print(Chat.find_attendees(from_client["token"],from_client["attendees"],from_client["create"],app))

# Key Actions

	if action == "set_key":
		print(OneTime.store_onetime(from_client["type"],from_client["register"],from_client["validusers"]))
	if action == "get_key":
		 print(Chat.get_key(from_client["token"],from_client["room"]))
		#print(OneTime.update_key(from_client["type"],from_client["register"],from_client["validusers"]))

# Connection Actions

	if action == "hive_connections":
		print(Connections.get_steem_connections(from_client["steem"]))
	if action == "openseed_connections":
		print(Connections.get_openseed_connections(from_client["account"],from_client["last"],from_client["count"],from_client["hive"]))
	if action == "profile_small":
		print(Connections.get_account(from_client["steem"]))
	if action == "profile":
		print(Connections.profile(from_client["token"]))
	if action == "get_profile":
		print("{"+Connections.user_profile(from_client["account"])+"}")
	if action == "send_request":
		print(Connections.connection_request(from_client["token"],from_client["account"],"request",app))
	if action == "set_request":
		print(Connections.connection_request(from_client["token"],from_client["account"],from_client["response"],app))
	if action == "get_requests":
		print(Connections.get_requests(from_client["token"],from_client["count"]))
	if action == "request_status":
		print(Connections.request_status(from_client["token"],from_client["account"]))

else:
	print("App rejected")

