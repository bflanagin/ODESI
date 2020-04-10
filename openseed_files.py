#!/usr/bin/python

import subprocess
import sys
import os
sys.path.append("..")
import mysql.connector
import socketserver
import openseed_account as Account
import openseed_seedgenerator as Seed
#import steem_get as Get
#import steem_submit as Submit
#import leaderboard as LeaderBoard
import openseed_music as Music
import openseed_setup as Settings
import json
import time
from bottle import route, run, template, get, post, request, static_file

settings = Settings.get_settings()

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='0.0.0.0', port=8689)
