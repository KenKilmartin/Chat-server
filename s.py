import socket
import threading, Queue
import hashlib
import time
from time import gmtime, strftime

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

def parseUsername(data):
    tempUser = data[6:len(data)]
    openingBracketPos = tempUser.index('<')
    name = tempUser[0: openingBracketPos]
    return name 

# custom say hello command
def sayHello():
    print "----> The hello function was called"

def getTime():
    conn.send("Current time is " + strftime("%a, %d %b %Y %H.%M.%S", gmtime()))

def parseMessage(command):
    print 'parsing message...'
    keyvaluePair = command[8: len(command)]

    dashPosition = keyvaluePair.index('_')
    hashed = keyvaluePair[dashPosition + 1:len(keyvaluePair)]

    message = keyvaluePair[0: dashPosition]
    hashedMessage = hashlib.sha224(message).hexdigest()
   
    if(hashedMessage in hashed):
        return message
    else:
        print 'hashes do not match'

def pong():
    print "sending pong..."
    start_time = time.time()
    conn.send("ping pong")

def count():
    buffer_string = str(buffer)
    stringArray = buffer_string.split("</cmd>")

    if len(stringArray) <= 0:
        conn.send("Number of messages -> 0")
    else:
        conn.send("Number of messages -> " + str(len(stringArray) - 1))
   
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
        command = data[start:-6] #-7 chops of the end of the tag </cmd>
        

        # Once we find a command, we will then check if a specific command
        # is inside, if we find the word "hello" we are telling the server
        # to call the sayHello() function.
        if "hello" in command:
            sayHello()

        if "message" in command:
            message = parseMessage(command)
            return message
        
        if "ping" in command:
            pong()

        if "total" in command:
            count()
        if "gettime" in command:
            getTime()

        
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
   # print 'Connected by', addr
    data = conn.recv(1024)
       
    name = ''
      
    if '<user>' in data:
        start_name = data.index('<user>')
        name = data[start_name + 6: -8]
        data = data[0:start_name]
    
    message = parseInput(data)# Calling the parser
    
    if message != '':
        print "rec:" + str(data)
        message = name + " says > " + message
        buffer += str(message)
    
    conn.send(str(buffer))
    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(1024)
    print data;

    if "<join>" in data:
        username = parseUsername(data)
        buffer += str(username + " has joined the conversation :")
      
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    


