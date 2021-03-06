#  coding: utf-8 
import SocketServer

# https://docs.python.org/2/library/os.path.html
import os.path

import time

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Preyanshu Kumar, Ryan Satyabrata
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2016 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Used for reference the http response standard https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html

class MyWebServer(SocketServer.BaseRequestHandler):

    requestHeader = []
    responseHeader=""
    contents=""
    
    def checkIsDir(self, pathStr):
        return os.path.isdir(os.curdir + pathStr)
        
    def checkIsFile(self, pathStr):

        return os.path.isfile(os.curdir + pathStr)

    def openTextFile(self, pathStr):
        file = open(pathStr[1:], 'r')
        return file.read()

    def openBinary(self, pathStr):
        file = open(pathStr[1:], 'rb')
        return file.read()
        
    def getDateTime(self):
        # https://docs.python.org/2/library/time.html#module-time
        # Format example Date (Must be in GMT): Tue, 15 Nov 1994 08:12:31 GMT
        dateTime = time.gmtime(time.time())
        dateTime = time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\r\n", dateTime)
        return dateTime;
        
    def mimeTypeGet(self, filepath):
        # Usually the extension is the last bit after the "."
        fileName = filepath.split('.')[-1]
        isText = True
        if (fileName == "html"):
            self.responseHeader += "Content-Type: text/html;\r\n"
        elif (fileName == "css"):
            self.responseHeader += "Content-Type: text/css;\r\n"
        elif (fileName == "jpg" or fileName == "jpeg"):
            isText = False
            self.responseHeader += "Content-Type: image/jpeg;\r\n"
        elif (fileName == "png"):
            isText = False
            self.responseHeader += "Content-Type: image/png;\r\n"
        elif (fileName == "gif"):
            isText = False
            self.responseHeader += "Content-Type: image/gif;\r\n"
        # Retrieve file size.
        self.responseHeader += "Content-Length: " + str(os.path.getsize(filepath[1:])) + "\r\n"
        # Load content
        if (isText):
            return self.openTextFile(filepath)
        elif (not isText):
            return self.openBinary(filepath)
    
    # Retrieves and access path. 
    # Assumes request header is a list splitted by space.
    def retrievePath(self, requestHeaderList):
        path = "/www/"
        if(len(requestHeaderList) > 1):
            path += requestHeaderList[1]
        # last / dir workaround for os.path.normpath
        endDirGood = False
        if(path[-1] == "/"):
            endDirGood = True
        # Normalize case, convert slashes, collapse redundant separators,
        # and removes up-level references. 
        # ALSO removes the very last / which is bad for dirs.
        # Normalized taken from python documentations
        # https://docs.python.org/2/library/os.path.html
        path = os.path.normpath(os.path.normcase(path))
        if(endDirGood):
            path += "/"
        # if a dir is given like this something.com/poo
        # make sure the dir will redirect to something.com/poo/
        # so that a file can be found inside the poo folder e.g. css or img
        if(os.path.isdir(os.curdir + path)):
            if(path[-1] != "/"):
                # Redirect to path with that / at the end of the url.
                path += "/"
                self.responseHeader += "HTTP/1.1 301 MOVED PERMANENTLY\r\n"
                self.responseHeader += "Location: " + path[4:] +"\r\n"
                return
            # Do not redirect for index.
            path += "index.html"
        #checking if it is a file and printing 200 code if it is ok
        if(os.path.isfile(os.curdir + path)):
            self.responseHeader += "HTTP/1.1 200 OK\r\n"
            #checking for mimetypes and reading them into content.
            self.contents = self.mimeTypeGet(path)
            
        else:
            self.responseHeader += "HTTP/1.1 404 NOT FOUND\r\n"
            self.responseHeader += "Content-Type: text/html;\r\n"
            self.contents = "<html><head></head><body><h1>404 NOT FOUND</h1></body></html>"
            
    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestHeader = self.data.split(" ")
        if(requestHeader[0].upper() == "GET"):
            self.retrievePath(requestHeader)
        else:
            self.responseHeader = "HTTP/1.1 501 NOT IMPLEMENTED\r\n"
        
        # All needs date according to 14.18 https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html 
        self.responseHeader += self.getDateTime();
                
        # sendall for tcp according to https://docs.python.org/2/library/socketserver.html#examples
        # Needs empty line to show end of header. Also using windows CR-LF new lines.
        self.request.sendall(self.responseHeader + "\r\n" + self.contents)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
