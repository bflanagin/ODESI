#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import hashlib
import json
import openseed_setup as Settings

settings = Settings.get_settings()

def get_curated_music(type):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE curation ='"+type+"' AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	for song in result:
		output.append({
			"author":song[0],
			"title": song[1],
			"post": song[2],
			"img": song[3],
			"ogg": song[4],
			"curation": song[5],
			"type": song[6],
			"genre": song[7],
			"tags": song[8],
			"duration": song[9]
			})
	music.close()
	openseed.close()
	return json.dumps(output)

def get_artist_tracks(artist):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE author =%s AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search,[artist])
	result = music.fetchall()
	for song in result:
		output.append({
			"author":song[0],
			"title": song[1],
			"post": song[2],
			"img": song[3],
			"ogg": song[4],
			"curation": song[5],
			"type": song[6],
			"genre": song[7],
			"tags": song[8],
			"duration": song[9]
			})
	music.close()
	openseed.close()

	return '{"author":"'+artists+'","tracks":['+json.dumps(output)+']}'

def get_new_artists():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE'_%' ORDER BY date DESC LIMIT 20"
	music.execute(search)
	result = music.fetchall()
	artist_num = 1
	for artist in result:
		if artist_num <= 5:
			if str(output).find(str(artist[0])) == -1:
				output.append(artist[0]) 
				artist_num +=1
		else:
			break
	music.close()
	openseed.close()
	
	return '{"new_musicians":'+json.dumps(output)+'}'

def get_new_tracks():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = ""
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC LIMIT 10"
	music.execute(search)
	result = music.fetchall()
	for song in result:
		if output.find(str(song)) == -1:
			dur = "0.00"
			if song[9] != None:
				dur = song[9].split(".")[0]+"."+song[9].split(".")[1][0:1]
			else:
				print(song[9])
			if output == "":
				output = '{"author":"'+song[0]+'","title":"'+song[1].replace('"','\\"').replace('"s ',"\\'s ")+'","post":"'+song[2]+'","img":"'+song[3]+'","ogg":"'+song[4]+'","curation":"'+str(song[5])+'","type":"'+song[6]+'","genre":"'+song[7]+'","tags":"'+song[8]+'","duration":"'+dur+'"}'
			else:
				output += ',{"author":"'+song[0]+'","title":"'+song[1].replace('"','\\"').replace('"s ',"\\'s ")+'","post":"'+song[2]+'","img":"'+song[3]+'","ogg":"'+song[4]+'","curation":"'+str(song[5])+'","type":"'+song[6]+'","genre":"'+song[7]+'","tags":"'+song[8]+'","duration":"'+dur+'"}'

	music.close()
	openseed.close()
	return '{"newtracks":['+output+']}'



def get_genres():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = ""
	search = "SELECT genre FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	for genre in result:
		if genre[0]:
			if str(output).find(genre[0]) == -1:
				if output == "":
					output += '{"name":"'+genre[0]+'","total":'+str(get_genre_totals(genre[0]))+'}'
				else:
					output +=  ',{"name":"'+genre[0]+'","total":'+str(get_genre_totals(genre[0]))+'}'

	music.close()
	openseed.close()
	return '{"genres":['+str(output)+']}'

def get_genre_totals(genre):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT genre FROM `audio` WHERE genre = %s AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	vals = (genre,)
	music.execute(search,vals)
	result = music.fetchall()
	
	music.close()
	openseed.close()
	return len(result)

def get_genre_tracks(genre,count):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	num = 0
	if count != "0":
		search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration,date FROM `audio` WHERE genre LIKE '"+genre+"' AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC LIMIT "+str(count)
	else:
		search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration,date FROM `audio` WHERE genre LIKE '"+genre+"' AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"

	music.execute(search)
	result = music.fetchall()
	num = 0
	for song in result:
		if song:
			output.append({
				"author":song[0],
				"title": song[1],
				"post": song[2],
				"img": song[3],
				"ogg": song[4],
				"curation": song[5],
				"type": song[6],
				"genre": song[7],
				"tags": song[8],
				"duration": song[9]
				})
	music.close()
	openseed.close()

	response = '{"genre_tracks":{"total":'+str(len(result))+',"results":'+json.dumps(output)+'}}'
	return response

def get_tracks(start = 0,count = 0):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	num = 0
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC LIMIT "+str(count)+" OFFSET "+str(start)
	music.execute(search)
	result = music.fetchall()
	
	for song in result:
		if song:
			output.append({
				"author":song[0],
				"title": song[1],
				"post": song[2],
				"img": song[3],
				"ogg": song[4],
				"curation": song[5],
				"type": song[6],
				"genre": song[7],
				"tags": song[8],
				"duration": song[9]
				})

	music.close()
	openseed.close()
	return '{"tracks":{"total":"'+str(len(result))+'","results":'+json.dumps(output)+'}}'

