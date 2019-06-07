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

def GetPage():
    file_content = ""

    with open('index.html', 'r') as file:
        file_content = "".join(file.readlines())
    
    return file_content


def UpdatePage(msg):
    with open('index.html', 'w') as file:
        file.write(GetTemplate().format(msg, GetKnownMessagesStr()))

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
        
        self.wfile.write(GetTemplate().format("", GetKnownMessagesStr()).encode())
    
    def do_POST(self):
        # Handle post requests
        
        #Decode form data
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # Check that the longuri and the shortname fields are filled
        if 'longuri' not in params or 'shortname' not in params:
            UpdatePage("Both fields need to be filled.")

            # Redirect the page back to the home page
            self.send_response(303)
            self.send_header('Location', "/")
            self.end_headers()

        # If both fields are filled, read the values
        longuri = params['longuri'][0]
        shortname = params['shortname'][0]

        if CheckURI(longuri):
            # URI is good, store the longuri and shortname
            memory[shortname] = longuri

            # Redirect to show the additional message
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # URI is bad, so don't store the data
            UpdatePage("The long URI was invalid. Please try a different one.")

            # Redirect to show the error message
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()


        
        
if (__name__ == '__main__'):
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()