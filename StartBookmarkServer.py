#!/usr/bin/env python3
#
# Author: Justin Tadlock
#
# This is a bookmark server that will maintain a mapping dictionary of long URI's and shortnames.

import http.server
import requests
from urllib.parse import unquote, parse_qs

def CheckURI(long_uri):
    try:
        data = requests.get(long_uri, timeout=5)
        return data.status_code == 200
    except:
        return False

def GetTemplate():
    with open('Template.html', 'r') as file:
        file_content = "".join(file.readlines())
    
    return file_content

class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle get requests
        self.send_response(200)
        
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(GetTemplate().format("","").encode())
    
    def do_POST(self):
        # Handle post requests
        stub = ""
        
if (__name__ == '__main__'):
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()