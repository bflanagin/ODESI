#!/usr/bin/python
import subprocess
import sys
import mysql.connector
import hashlib
import os
sys.path.append("..")
import openseed_setup as Settings


def store_key(account,key):

	process = subprocess.Popen(['hivepy', 'addkey', key], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	print(stdout)

def import_account(acount,masterpass):
	process = subprocess.Popen(['echo',masterpass,'|','hivepy', 'importaccount', account], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	print(stdout)
	
def flush_keys(account):
	keys = find_keys_by_accountname(account)
	for key in keys:
		process = subprocess.Popen(['echo','Y','|','hivepy', 'delkey', key], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	print(stdout)

def allow_app(account,app,allowed):
	if allowed == "posting" or allowed == "active":
		process = subprocess.Popen(['hivepy', 'allow', '--account', account,'--permission',allowed,app], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		process.wait()
		stdout, stderr = process.communicate()
	
def disallow_app(account,app,remove):
	if remove == "posting" or remove == "active":
		process = subprocess.Popen(['hivepy', 'disallow','--account', account,'--permission',remove,app], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		process.wait()
		stdout, stderr = process.communicate()
	
def verify_user(account,postingkey):
	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()

def openseed_interconnect(account,postkey):

	process = subprocess.Popen(['hivepy', 'pin', 'ls', '--type', 'recursive', thehash], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	
def find_keys_by_accountname(account):
	process = subprocess.Popen(['hivepy', 'listaccounts'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	process.wait()
	stdout, stderr = process.communicate()
	keys = []
	for line in stdout.decode().split("\n"):
		if line.find("|") != -1:
			if line.find(account) != -1:
				print(line)
				keys.append(line.split("|")[3].strip())
	return keys

