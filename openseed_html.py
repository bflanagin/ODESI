#!/usr/bin/python

import sys
sys.path.append("..")
import socketserver
import http.server
Handler = http.server.SimpleHTTPRequestHandler

class TCPHandler(http.server.SimpleHTTPRequestHandler):
	print("Hello")

if __name__=="__main__":
	HOST1, PORT1 = "0.0.0.0",8689
	with socketserver.TCPServer((HOST1, PORT1), TCPHandler) as httpd:
    		print("serving at port", PORT1)
    		httpd.serve_forever() 
