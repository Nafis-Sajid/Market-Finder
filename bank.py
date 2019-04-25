import sys
import socket
import json           
  
#a socket object 
s = socket.socket()          
print ("Socket for Bank successfully created")
  
# reserve BANK_PORT from input argument for banking purpose 
BANK_PORT = int(sys.argv[1])

# Next bind to the BANK_PORT 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', BANK_PORT))         
print ("socket binded to %s" %(BANK_PORT) )
  
# put the socket into listening mode 
s.listen(5)      
print ("socket is listening")
  
# a forever loop until we interrupt it or an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got data from', addr)

   #receive byte from server and decode it into string
   received = c.recv(1024).decode("utf-8")
   #convert into dictionary
   received_info = json.loads(received)
   print(received_info)
  
   # send a thank you message to the client.  
   c.send(bytes('Thank you for connecting', "utf-8")) 
   
   # Close the connection with the client 
   c.close() 