import socket
import threading
import time
import sys
from _thread import *

name = ""

# thread fuction 
def threaded(c): 
 
    while (c): 
        try: 
            msg = c.recv(1024).decode() + "\n~~~"
            print(msg) 
            if msg.find("would") !=-1: # check if we have a chat request
                start_new_thread(threaded, (c,)) # recursively create a new thread to keep listening
                self.join() # end this current thread to be able to start chatting
                
        except:
            break
        



    
def printMenu(name):
    print("\n********************************\n")
    print("Logged in as: " + name + " || Menu: \n")
    print("--------------------------------\n")
    print("1 - List Users\n")
    print("2 - Chat \n")
    print("3 - Quit\n") 
    print("********************************\n") 

def chat(s):
    # simple function but helps with all the send /recv 's
    target = input("> ") 
    s.send(target.encode())

    
    
        

    
def Main():

    # Connection setup.
    s = socket.socket()
    port = 25565                
    s.connect(('127.0.0.1', port))  

    # Enter the room.
    namepass = s.recv(1024).decode()
    
    while namepass != "true":
        print("Enter a username:")
        name = input(">")
        s.send(name.encode())
        namepass = s.recv(1024).decode()

    # a forever loop until client wants to exit 
    start_new_thread(threaded, (s,)) 
    dont_print = False
    
    while True: 

        time.sleep(.2) # sleep so that the listening thread can print out before
        
        if dont_print == False: # to prevent printing the menu when clients are chatting
            printMenu(name)
        else:
            dont_print = False # anticipate printing next loop
            
        
        mes = input("> ")
       
        # check what type of msg we have and send it to server
        if mes == "1":
            print("Here are the users: ")
            s.send((name + ": " + mes).encode())

           
        elif mes == "2":
            dont_print = True
            s.send((name + ": " + mes).encode())
            print("Who would you like to chat with?")
            chat(s)
            
        elif mes == "3":
            s.send((name + ": " + mes).encode())
            break
            
        else: # if not 1,2,3 then we assume chatting / no cmd
            dont_print = True
            s.send((name + ": " + mes).encode())
            print("")
            
        
    s.send("3".encode())
    s.close() 
    print("Exiting...")


if __name__ == '__main__': 
	Main() 