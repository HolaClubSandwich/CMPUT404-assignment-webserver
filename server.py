#  coding: utf-8 
import socketserver
import os

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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_string = self.data.decode('utf-8')
        request = data_string.split('\r\n')[0]
        http_command, path, _ = request.split(' ')
        print("HTTP COMMAND: ", http_command)
        print("Path: ", path)
        


        if data_string != None:
            if http_command != 'GET':
                self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
            elif '.' not in path.split('/')[-1] and path[-1] != '/':
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + path + '/' + "\r\n", 'utf-8'))

            else:
                self.server_support(path)
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
            

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK\r\n",'utf-8'))

    def server_support(self, path):
        starting_path = './www'
        if os.path.realpath(os.getcwd() + starting_path + path).startswith(os.getcwd() + starting_path):
            if os.path.exists(starting_path + path + "/index.html") and path.endswith('/'):
                data = open(starting_path + path + "/index.html").read()
                if data != None:
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + data, 'utf-8'))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
            elif os.path.exists(starting_path + path) and path.endswith(".html"):
                data = open(starting_path + path).read()
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + data, 'utf-8'))
            elif os.path.exists(starting_path + path) and path.endswith(".css"):
                data = open(starting_path + path).read()
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + "Content-Type: text/css\r\n" + data, 'utf-8'))
            else:
                try:
                    data = open(starting_path + path + "/index.html")
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + path + '/' + "\r\n", 'utf-8'))
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
