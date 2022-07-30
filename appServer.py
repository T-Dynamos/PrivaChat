import socket
import threading
import sys

clients = [] 
nicknames = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_server(port,print_message,close_request,host="127.0.0.1",*largs) -> None:
	server.bind((host,port))
	server.listen()
	print_message("Server started on :"+str(port))
	while True:
		try:
			client, address = server.accept()  
			client.send('NICK'.encode('ascii'))                      
			nickname = client.recv(1024).decode('ascii')               
			nicknames.append(nickname)
			clients.append(client)
			print_message("{} Joined {}".format(str(nickname),str(address)))
			thread = threading.Thread(target=handle, args=(client,))   
			thread.start()  
		except Exception as e:
			close_request()


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

def stop_server() -> None:
	server.shutdown(socket.SHUT_RDWR)
	server.close()


def handle_client(	nickname,
					send_message,
					recieve_message,
					port,
					addr,
					shutdown,
					*largs)	:

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((addr, int(port)))

	def sendMessage(msg,*largs):
		send_message()

		client.send(str(msg+" nicksignal "+nickname).encode('ascii'))

	def recieveMessage(*largs):
		while True:
			print("Connection started")
			message = client.recv(1024).decode('ascii')
			if message == "NICK":
				client.send(nickname.encode('ascii'))
			else:
				nickname_2 = message.split("nicksignal")[-1]
				print(nickname_2,nickname)
				if nickname_2.replace(" ","") != nickname.replace(" ",""):
					recieve_message(message.split("nicksignal")[0],nickname_2)
			print("Connection complete :"+message)

	return sendMessage,recieveMessage



