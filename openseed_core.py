#!/usr/bin/python3

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver

import openseed_account as Account
import openseed_connections as Connections
import openseed_seedgenerator as Seed
import openseed_utils as Utils
import openseed_music as Music
import openseed_setup as Settings
import openseed_game as Game
import openseed_chat as Chat
import onetime as OneTime
import openseed_hive as Hive


import json
import time
from bottle import route, run, template, request, static_file

settings = Settings.get_settings()


def message(data):
	response = "Please issue a command to continue"
	try:
		from_client = json.loads(data)
	except:
		return '{"server":"messages must be in json formated string"}'
	else:		
		action = from_client["act"]
		if Account.check_appID(from_client["appPub"],from_client["devPub"]):
			app = from_client["appPub"]
			dev = from_client["devPub"]
			
			

			#####################################################
			#
			#  Account Section
			#
			#####################################################

			if action == "account_check":
				response = Account.accountCheck(from_client["account"],from_client["passphrase"])
			elif action == "creator_check":
				response = Account.creator_check(from_client["openseed"])
			elif action == "create_account":
				response = Account.create_account(from_client["account"],from_client["passphrase"],from_client["email"])
			
			elif action == "create_creator_account":
				response = Account.create_creator(from_client["creatorName"],from_client["contactName"],from_client["contactEmail"],from_client["openseed"])
			elif action == "set_profile":
				response = Account.set_profile(from_client["token"],from_client["data1"],from_client["data2"],
					from_client["data3"],from_client["data4"],from_client["data5"],from_client["type"])
			elif action == "get_status":
				response = Account.get_status(from_client["account"])
			elif action == "set_status":
				response = Account.set_status(from_client["appPub"],from_client["token"],from_client["status"])
			elif action == "get_history":
				response = Account.get_history(from_client["account"],from_client["apprange"],from_client["count"])
			elif action == "update_history":
				response = Account.update_history(from_client["account"],from_client["type"],from_client["appPub"],from_client["data"])

			#####################################################
			#
			#  Hive Section
			#
			#####################################################

			elif action == "hive_send_payment":
				response = Hive.payment(from_client["hiveaccount"],from_client["to"],from_client["amount"],from_client["for"],from_client["postingkey"])
			elif action == "hive_flush_keys":
				response = Hive.flush_account(from_client["hiveaccount"])
			elif action == "hive_login":
				response = Hive.openseed_interconnect(from_client["hiveaccount"],from_client["hiveaccount"],from_client["postingkey"],from_client["storekey"])
			elif action == "hive_connect":
				response = Hive.openseed_interconnect(from_client["account"],from_client["hiveaccount"],from_client["postingkey"],from_client["storekey"])
			elif action == "get_hive_account":
				response = Hive.get_account(from_client["account"])
			elif action == "get_full_hive_account":
				response = Hive.get_full_account(from_client["account"])
			elif action == "get_hive_post":
				response = Hive.get_post(from_client["author"],from_client["permlink"])
			elif action == "set_posting_right":
				response = '{"server":"error"}'
			elif action == "remove_posting_right":
				response = '{"server":"error"}'
			elif action == "link_account":
				response = Account.hive.link(from_client["username"],from_client["hivename"])
				if response:
					Hive.memo(from_client["username"],from_client["hivename"],response)

			#####################################################
			#
			#  Games Section
			#
			#####################################################

			elif action == "update_leaderboard":
				response = Game.update_leaderboard(dev,app,from_client["username"],from_client["data"],from_client["hive"],from_client["postingkey"])
			elif action == "get_leaderboard":
				response = Game.get_leaderboard(dev,app)

			#####################################################
			#
			#  Music Section
			#
			#####################################################

			elif action == "music":
				response = Music.get_curated_music_json(from_client["curator"])
			elif action == "artist_search":
				response = Hive.search_music(from_client["author"],10000)
			elif action == "get_new_musicians":
				response = Music.get_new_artists()
			elif action == "get_new_tracks":
				response = Music.get_new_tracks_json()
			elif action == "get_genres":
				response = Music.get_genres()
			elif action == "get_genre":
				response = Music.get_genre_tracks_json(from_client["genre"],from_client["count"])
			elif action == "get_artist_tracks":
				response = Music.get_artist_tracks_json(from_client["author"],from_client["count"])
			elif action == "get_tracks":
				response = Music.get_tracks_json(from_client["start"],from_client["count"])

			#####################################################
			#
			#  Connections Section
			#
			#####################################################

			elif action == "get_connections":
				response = Connections.get_openseed_connections(from_client["account"],from_client["hive"])
			elif action == "get_profile":
				response = "{"+Account.get_profile(from_client["account"])+"}"
			elif action == "get_requests":
				response = Connections.get_requests(from_client["token"],from_client["count"])
			elif action == "send_request":
				response = Connections.connection_request(from_client["token"],from_client["account"],"request",app)
			elif action == "set_request":
				response = Connections.connection_request(from_client["token"],from_client["account"],from_client["response"],app)
			elif action == "get_request_status":
				response = Connections.request_status(from_client["token"],from_client["account"])

			#####################################################
			#
			#  Chat Section
			#
			#####################################################

			elif action == "get_conversations":
				response = Chat.get_conversations(from_client["token"])
			elif action == "create_chatroom":
				response = Chat.create_chatroom(from_client["token"],from_client["title"],from_client["attendees"],app)
			elif action == "get_chat_history":
				response = Chat.get_chat_history(from_client["token"],from_client["room"],from_client["count"],from_client["last"])
			elif action == "get_chat":
				response = Chat.get_chat(from_client["token"],from_client["room"],from_client["last"])
			elif action == "send_chat":
				response = Chat.send_chat(from_client["token"],from_client["room"],from_client["message"],app)
			elif action == "find_room_by_attendees":
				response = Chat.find_attendees(from_client["token"],from_client["attendees"],from_client["create"],app)

			elif action == "set_key":
				response = OneTime.store_onetime(from_client["type"],from_client["register"],from_client["validusers"])
			elif action == "get_key":
				response = OneTime.get_key(from_client["thetype"],from_client["token"],from_client["room"])

			# Heart Beat #	
			elif action == "heartbeat":
				response = "Online"

			# Utils #
			elif action =="get_image":
				response = Utils.get_image(False,from_client["image"],from_client["thetype"],from_client["quality"])
				
		else:
			response = "App rejected"

	return response

