#!/usr/bin/python
import sys
import mysql.connector
import hashlib
import os
sys.path.append("..")
import openseed_setup as Settings


def hive_store_key(account,key):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	
def hive_flush_keys(account):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()

def hive_allow_app(account,app,allowed):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	
def hive_disallow_app(account,app,remove):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	
def hive_verify_user(account,postingkey):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()

def hive_openseed_interconnect(account,postkey):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
