#  coding: utf-8 
import SocketServer

# https://docs.python.org/2/library/os.path.html
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# http response standard https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html

class MyWebServer(SocketServer.BaseRequestHandler):

    requestHeader = []
    responseHeader="HTTP/1.1 "
    

    def checkIsDir(self, pathStr):
        return os.path.isdir(os.curdir + pathStr)
        
    def checkIsFile(self, pathStr):

        return os.path.isfile(os.curdir + pathStr)

    def openTextFile(self, pathStr):
        file = open(pathStr[1:], 'r')
        return file.read()

    def mimeTypeCheck(self, fileName):
        if (fileName[1] == "html"):
            self.responseHeader += "Content-Type: text/html;"
        elif (fileName[1] == "css"):
            self.responseHeader += "Content-Type: text/css;"
        
    # Retrieves and access path. 
    # Assumes request header is a list splitted by space.
    def retrievePath(self, requestHeaderList):
        path = "/www/"
        if(len(requestHeaderList) >=1):
            path += requestHeaderList[1]
        # normalize case, convert slashes, collapse redundant separators,
        # and removes up-level references.
        path = os.path.normpath(os.path.normcase(path))
        #handle the 404 (technically 403 but 404 is safer): path - os.curdir if it is not www/ then call error!
        
        # if a dir is given like this something.com/poo
        # make sure the dir will redirect to something.com/poo/
        # so that a file can be found inside the poo folder e.g. css or img
        if(os.path.isdir(os.curdir + path)):
            #better to post a 302 and redirect.
            path += "/index.html"
        contents = ""
        #check if file or dir exist.
        print("Path request is: " + path + "\n")
        #checking if it is a file and printing 200 code if it is ok
        if(os.path.isfile(os.curdir + path)):
            self.responseHeader += "200 OK\r\n"
            fileName = path.split('.')
            #checking for mimetypes
            self.mimeTypeCheck(fileName)
            file = open(path[1:], 'r')
            contents = file.read()
        else:
            self.responseHeader += "404 NOT FOUND\r\n"
        return contents
            
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        print "Client address: %s" % self.client_address[0]
        
        requestHeader = self.data.split(" ")
        
        responseContent = ""        
        responseContent = self.retrievePath(requestHeader)

        # sendto for udp.
        #self.request.sendto("hi", self.client_address)
        
        # sendall for tcp according to https://docs.python.org/2/library/socketserver.html#examples
        # Needs empty line to show end of header. Also using windows CR-LF new lines.
        self.request.sendall(self.responseHeader + "\r\n\r\n" + responseContent)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
