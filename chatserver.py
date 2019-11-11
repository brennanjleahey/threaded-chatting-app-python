# import socket programming library 
import socket
import threading
import sys
import time 

from _thread import *

CHAT = [] # for storing sockets of chatting clients

USER_INFO = dict() # for all clients' data

def name_init(c,addr):

    namepass = "false"
    c.send(namepass.encode()) 
    
    while namepass != "true": # namepass acts as a flag
        uname = c.recv(1024).decode()
        if uname not in USER_INFO: # if name not taken, store info        
            
            USER_INFO[uname] = {}
            USER_INFO[uname]["username"] = uname
            USER_INFO[uname]["socket"] = c
            USER_INFO[uname]["Avalible/Busy"] = "Avalible"       
            
            namepass = "true" # break the loop
               
                
        c.send(namepass.encode())  # send namepass result either case   

    return uname
            
def talk_to(c,curr_username):

    #send over user list
    list_avail_users(c,curr_username)
    target = c.recv(1024).decode()
    target = target.strip()

    if target.find(curr_username) != -1: 
        c.send('Error. You cannot talk to yourself'.encode())
        
    else:
        print('**Request: ',curr_username,' Wants to talk to ',target)

        if target in USER_INFO:
            if USER_INFO[target]["Avalible/Busy"] == "Avalible":
                print(target, 'is valid.')
                target_socket = USER_INFO[target]["socket"]
                target_socket.send('Incoming request'.encode())
                prompt = curr_username + ' would like to chat. Hit enter then Enter yes/no'
                target_socket.send(prompt.encode())
                answer = target_socket.recv(1024).decode()
                print(target,' replied:: ', answer)

                if answer.find('Yes') != -1 or answer.find('yes') != -1:
                    print('Connecting ',curr_username, ' with ',target)
                    CHAT.append(target_socket)
                    CHAT.append(c)
                    prompt = "Starting private chat with " + target
                    c.send(prompt.encode())
                    prompt = "Starting private chat with " + curr_username
                    target_socket.send(prompt.encode())
                    USER_INFO[curr_username]["Avalible/Busy"] = "Busy chatting w/ " + target
                    USER_INFO[target]["Avalible/Busy"] = "Busy chatting w/ " + curr_username
                    
                else:
                    target_socket.send('Chat failed.'.encode())
                    c.send('Chat failed.'.encode())
        else:
            c.send('Could not find user.'.encode())
                   

def list_users(c):
    uList = ""

    for index in USER_INFO:
        uList += f'{index}' + " " + f'{USER_INFO[index]["Avalible/Busy"]}' + '\n'    

    c.send(uList.encode())

def list_avail_users(c,curr_username):
    uList = ""
    for index in USER_INFO: # send over user list of avalible users
        if USER_INFO[index]["Avalible/Busy"] == "Avalible" and USER_INFO[index] != curr_username:
            uList += f'{index}' + " " + f'{USER_INFO[index]["Avalible/Busy"]}' + '\n'

    c.send(uList.encode())
    
# thread fuction 
def threaded(c,addr): 
    
    try: # try catch so server won't crash
        curr_username = name_init(c,addr)
    
    # Print Current Users
        print("Current User List: ")
        for x in USER_INFO:
            print(x)
            
        while True: 

            # data received from client 
            
            data_raw = c.recv(1024)
            data = data_raw.decode()
            print(data)

            if data.find("1") != -1:
                print(data + " - List users request")
                list_users(c)
            
            
            elif data.find("2") != -1:
                print(data + " - Chat request")
                talk_to(c,curr_username)
                print("Finished chat function")
                    
            
            elif data.find("3") != -1:
                
                print(curr_username + " - Disconnect")
                del USER_INFO[curr_username]
                c.close()
                #USER_INFO[curr_username]["Avalible/Busy"] = "Offline" 
                break    
            
            else:
                if not data: 
                    print('Bye')
                    del USER_INFO[curr_username]
                    #USER_INFO[curr_username]["Avalible/Busy"] = "Offline" 
               
                
                
            for client in CHAT:
                try:
                    if client != c:
                        client.send(data_raw)
                except Exception as ex:
                    print(ex)
                    CHAT.remove(client)
         
    except Exception as ex:
        print(ex)
        if curr_username in USER_INFO:
            del USER_INFO[curr_username]
            #USER_INFO[curr_username]["Avalible/Busy"] = "Offline" 

def Main(): 
# initialize host and port
    host = "" 

    port = 25565 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 

	# put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 

    
	# loop until client wants to exit 
    while True: 
    
        # establish connection with client 
        c, addr = s.accept() 
        start_new_thread(threaded, (c,addr)) 
        
		# lock acquired by client 
        print('Connected to :', addr[0], ':', addr[1])

    s.close()    
    
     


if __name__ == '__main__': 
	Main() 