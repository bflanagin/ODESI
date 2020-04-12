#!/usr/bin/python
import sys
sys.path.append("..")
import mysql.connector
import hashlib
import json
import openseed_setup as Settings

settings = Settings.get_settings()


