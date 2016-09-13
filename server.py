#  coding: utf-8 
import SocketServer

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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall("Socket works.")
        print "Client address: %s" % self.client_address[0]
        #just put response in sendall? IT WORKS!
        self.request.sendall("""HTTP/1.1 200 ok\n\n<!DOCTYPE html>
            <html>
            <head>
                <title>Example Page</title>
                    <meta http-equiv="Content-Type"
                    content="text/html;charset=utf-8"/>
                    <!-- check conformance at http://validator.w3.org/check -->
                    <link rel="stylesheet" type="text/css" href="base.css">
            </head>

            <body>
                <div class="eg">
                    <h1>An Example Page</h1>
                    <ul>
                        <li>It works?
                                    <li><a href="deep/index.html">A deeper page</a></li>
                    </ul>
                </div>
            </body>
            </html> 
        """)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
