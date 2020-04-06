#!/usr/bin/python

import mysql.connector
import hashlib
import random
import sys
sys.path.append("..")
import openseed_seedgenerator as Seed
from steem import Steem
thenodes = ['anyx.io','api.steem.house','hive.anyx.io','steemd.minnowsupportproject.org','steemd.privex.io']
s = Steem()

import openseed_setup as Settings

settings = Settings.get_settings()

#Using the schema id we generate the token.
def create_nft(schema_id):

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

	return

def buy_nft(tokenId,account,price):

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

	return

def sale_nft(tokenId,account,price):

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

	return

# Trades are handled user acount to account where the account asking must own "this_tokenId" but not the "for_tokenId". Once a trade has started the asset is locked until the response comes in. The owners of either token can cancel or deny the trade but cannot trade the asset multiple times.
def trade_nft(this_tokenId,account,for_tokenId,response):

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

	return

# The NFT Schema is used to create the NFTs on demand. The record is kept on OpenSeeds server but could be shared on steem at a later date.
# The unique_data field will be used for the tokens unique fields. In the case of the schema these will be structured like this {<var name>:{begin:<num>,end:<num>}} the generator will read these keys and generate a value for the variable name in the final token.   

def create_nft_schema(creator_id,version,type,preview,asset,unique_data,discription,upgradeable,license,license_file,total_available):

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

	return
