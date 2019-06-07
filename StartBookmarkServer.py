#!/usr/bin/env python3
#
# Author: Justin Tadlock
#
# This is a bookmark server that will maintain a mapping dictionary of long URI's and shortnames.

import http.server
import requests
from urllib.parse import unquote, parse_qs

memory = {}

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

def GetKnownMessagesStr():
    known = "".join(
        "<tr>\n\t\t\t\t"
        "<td style=\"border: 1px solid black;\">{}</td>\n\t\t\t\t"
        "<td style=\"border: 1px solid black;\">\n\t\t\t\t\t"
        "<a href=\"{}\" target=\"_blank\">{}</a>\n\t\t\t\t"
        "</td>\n\t\t\t"
        "</tr>\n\t\t\t".format(key, memory[key], memory[key])
                    for key in sorted(memory.keys()))
    return known

class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle get requests
        self.send_response(200)
        
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(GetTemplate().format("",GetKnownMessagesStr()).encode())
    
    def do_POST(self):
        # Handle post requests
        stub = ""
        
if (__name__ == '__main__'):
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()