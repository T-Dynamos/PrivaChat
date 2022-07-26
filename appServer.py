import socket
import threading
import sys

clients = [] 
nicknames = []

def start_server(port,print_message,host="127.0.0.1") -> None:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host,port))
	server.listen()
	while True:
		client, address = server.accept()  
		client.send('NICK'.encode('ascii'))                        
		nickname = client.recv(1024).decode('ascii')                
		nicknames.append(nickname)
		clients.append(client)
		print_message("{} Connected with {}".format(str(nickname),str(address)))
		broadcast("{} joined!".format(nickname).encode('ascii'))   
		client.send('Connected to server!'.encode('ascii'))        
		thread = threading.Thread(target=handle, args=(client,))   
		thread.start()  

def broadcast(message): 
    for client in clients:
        client.send(message)                                        

def handle(client):
    while True:
        try:
            message = client.recv(1024)                      
            broadcast(message)                                      
        except:
            index = clients.index(client)        
            clients.remove(client)       
            client.close()
            nickname = nicknames[index]                             
            broadcast('{} left!'.format(nickname).encode('ascii'))  
            nicknames.remove(nickname)
            break
