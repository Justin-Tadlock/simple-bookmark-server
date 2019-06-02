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
    # Stub for reading the Template.html file and returning the contents as a string
    
class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle get requests
        
    def do_POST(self):
        # Handle post requests
        
    
if(__name__ == '__main__'):
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()