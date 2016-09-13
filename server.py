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
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        print "Client address: %s" % self.client_address[0]
        
        requestHeader = self.data.split(" ")
        
        responseHeader = "HTTP/1.1 200 ok"
        
        path = "/www/" 
        if(len(requestHeader) >=1):
            path += requestHeader[1]
        # normalize case and convert slashes, and collapse redundant separators.
        path = os.path.normpath(os.path.normcase(path))
        print("\n" + path + " \n")
        print(os.curdir + path + " \n")
        
        #handle the 404 (technically 403 but 404 is safer): path - os.curdir if it is not www/ then call error!
        
        if(os.path.isdir(os.curdir + path)):
            #better to post a 302 and redirect.
            path += "/index.html"
        contents = ""
        #file = open("www/index.html", 'r')
        #contents = file.read()
        #check if file or dir exist.
        if(os.path.isfile(os.curdir + path)):
            print("aaa" + "\n")
            file = open(path[1:], 'r')
            contents = file.read()
        # sendto for udp.
        #self.request.sendto("hi", self.client_address)
        # sendall for tcp according to
        # https://docs.python.org/2/library/socketserver.html#examples
        self.request.sendall(responseHeader + "\n" + contents)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
