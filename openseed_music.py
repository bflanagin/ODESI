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
	output = "{"
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE curation ='"+type+"' AND ogg IS NOT NULL AND ogg LIKE '_%'"
	music.execute(search)
	result = music.fetchall()
	for song in result:
		output = output + str(song).replace("'s","s").replace('"',"'").replace("'t","t") + "},{" 
	output = output+"}"
	music.close()
	openseed.close()
	return str(output)

def get_curated_music_json(type):
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
	output = "{"
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE author =%s AND ogg IS NOT NULL AND ogg LIKE '_%'"
	music.execute(search,[artist])
	result = music.fetchall()
	for song in result:
		output = output + str(song).replace("'s","s").replace('"',"'") + "},{"
	output = output+"}"
	music.close()
	openseed.close()
	
	return str(output)

def get_artist_tracks_json(artist):
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

	return json.dumps(output)

def get_new_artists():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE'_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	artist_num = 1
	for artist in result:
		if artist_num <= 5:
			if str(output).find(str(artist)) == -1:
				output.append(artist) 
				artist_num +=1
		else:
			break
	music.close()
	openseed.close()
	
	return str(output)

def get_new_tracks():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	artist_num = 1
	for artist in result:
		if artist_num <= 15:
			if str(output).find(str(artist)) == -1:
				output.append(artist) 
				artist_num +=1
		else:
			break
	music.close()
	openseed.close()
	return str(output)


def get_new_tracks_json():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	artist_num = 1
	for song in result:
		if artist_num <= 15:
			if str(output).find(str(song)) == -1:
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
				artist_num +=1
		else:
			break
	music.close()
	openseed.close()
	return json.dumps(output)



def get_genres():
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT genre FROM `audio` WHERE ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	for genre in result:
		if genre[0]:
			if str(output).find(genre[0]) == -1:
				output.append(genre) 

	music.close()
	openseed.close()
	return str(output)

def get_genre_tracks(genre):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE genre LIKE '"+genre+"' AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	for genre in result:
		if genre:
			output.append(genre) 

	music.close()
	openseed.close()
	return str(output)

def get_genre_tracks_json(genre):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["ipfsuser"],
		password = settings["ipfspassword"],
		database = "ipfsstore"
		)
	music = openseed.cursor()
	output = []
	search = "SELECT author,title,post,img,ogg,curation,type,genre,tags,duration FROM `audio` WHERE genre LIKE '"+genre+"' AND ogg IS NOT NULL AND ogg LIKE '_%' ORDER BY date DESC"
	music.execute(search)
	result = music.fetchall()
	for genre in result:
		if genre:
			output.append({
					"author":genre[0],
					"title": genre[1],
					"post": genre[2],
					"img": genre[3],
					"ogg": genre[4],
					"curation": genre[5],
					"type": genre[6],
					"genre": genre[7],
					"tags": genre[8],
					"duration": genre[9]
					})

	music.close()
	openseed.close()
	return json.dumps(output)

