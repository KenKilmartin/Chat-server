import socket
import threading, Queue
import hashlib



HOST = '127.0.0.1'        
PORT = 50007              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


  
    
# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""   

# custom say hello command
def sayHello():
    print "----> The hello function was called"
	
def parseMessage(command):
    print "parsing message..."
	#removing the word "message:" (8 chars)
    keyvaluePair = command[8:len(command)]
	
    print "full string: "+ str(keyvaluePair)
    
    dashPosition = keyvaluePair.index('-')
    hash = keyvaluePair[dashPosition+1:len(keyvaluePair)]
    
    message = keyvaluePair[0:dashPosition]
    print "message is: "+ message
    newhash = hashlib.sha224(message).hexdigest()
    print "Data rec hashed: "+str(newhash)
    print "the hash is... "+str(hash)
    
  
  
def pong():
    print "sending pong"
    conn.send("pong")

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data):
    print "parsing..."
    print str(data)
    
    # Checking for <cmd> commands
    if "cmd" in data:
        print "command in data.."
        
        # find the start position index of the command
        start = data.index('<cmd>')
        # Add 5 on for the length of the <cmd>
        start = start + 5
        # chop up remving start and end. 
        command = data[5:-7] #-7 chops of the end of the tag </cmd>
        
        # Once we find a command, we will then check if a specific command
        # is inside, if we find the word "hello" we are telling the server
        # to call the sayHello() function.
        if "hello" in command:
            sayHello()
        elif "message" in command:
		    parseMessage(command)
        elif "ping" in command:
		    pong()
        
    
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
    print 'Connected by', addr
    
    
    data = conn.recv(1024)
    
    parseInput(data)# Calling the parser
    
    print "rec:" + str(data)
    buffer += str(data)
    
    conn.send(str(buffer))
        
    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    


