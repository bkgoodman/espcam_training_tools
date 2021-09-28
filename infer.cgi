#!/usr/bin/python3

import os,sys,socket,cgi


# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = './infer_socket'
try:
    sock.connect(server_address)
except BaseException as msg:
    print( msg)
    sys.exit(1)

form=cgi.FieldStorage()

sock.sendall(form['path'].value.encode('utf-8'))
result = sock.recv(256)
print ("""Content-type: application/json

""")
print (result.decode('utf-8'))
