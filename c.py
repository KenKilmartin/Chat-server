
# Echo client program
import socket
import threading, Queue
import hashlib
import time

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server


print "What is your user name:"
username = raw_input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send("<join>" + username + "</join>")

# ==
print "type input:"
text = raw_input()

if "ping" in text:
	start_time = time.time()
	print "ping started ->" + str(start_time)



# when we send data to the server, we are using a colon
# at the end of a sentence to mark the end of the current sentence
# later when the input comes back, we will then be breaking the input
# into individual parts using the colon : to separate the lines

hash = hashlib.sha224(text).hexdigest()
output = '<cmd>message:'+ text + '_' + hash + '</cmd><user>' + username + '</user>'# command

if "ping" in text:
	output =  "<cmd>ping</cmd>"

if "total" in text:
	output =  "<cmd>total</cmd>"

if "gettime" in text:
	output =  "<cmd>gettime</cmd>"

s.sendall(output + ":")

data = s.recv(80000)

# breaking apart the data we get back.
response = data.split(':')

for x in response:
    print "Response:" + str(x)

if "ping pong" in response:
	stop_time = time.time()
	trip_time = stop_time-start_time
	print "stop time " + str(stop_time)
	print str(trip_time) + " secs to reply"
    
s.close()



