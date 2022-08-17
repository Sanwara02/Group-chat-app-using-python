#SERVER BASED GROUP CHAT APPLICATION
#edited by: Sanwara J. Chandak 
'''----------------------------'''


import socket 
import threading 

'''here, loacalhost IP address is used as we want to run the server as well as client on the same device.
if we want to connect the server and client on two different devices, the ip address of the host needs to be provided
we can easily find out the IP address of the device by running the ipconfig command in command prompt and then selecting the IPv4 address'''

host='127.0.0.1'


'''socket address= IP address:port no.;  in this project, socket address= 127.0.0.1:9090
In order to connect server and client, port number is required, any port number of value between 1025 to 65535 can be used
port no. from 0-1024 are reserved
checkout for winerror 10053'''

port=9090  

'''for TCP model use SOCK_STREAM and for UDP use SOCK_DGRAM, TCP is more reliable. UDP can be used 
for video calling applications'''

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   


server.bind((host,port))
server.listen()                                                     #server will listen for active connections

clients=[]                                                          #to keep a track of connected users
usernames=[]

def broadcast(message):                                             #displaying messages to all connected clients
    for client in clients:
        client.send(message)

def handle_client(client):                                          #handling messages from clients
    while True:                                                     #to run the infinite loop
        try:
            message= client.recv(1024)
            print(f'{usernames [clients.index(client)]} : {message}')
            broadcast(message)

        except:
            index=clients.index(client)  
            clients.remove(client)                                   #removing client from clients list if connection is closed
            client.close()
            username=usernames[index]
           
            usernames.remove(username)
            break                                                    #to come out of infinte loop

def recieve():                                                       #handling the connected clients
    while True:
        client, address= server.accept()
       
        print("connected with", address)                             #visible only on server side

        client.send('USER'.encode('utf-8'))
        username=client.recv(1024)

        usernames.append(username)
        clients.append(client)

        print("Username of the client is", username)
        broadcast(f'{username}\n' .encode('utf-8'))

        '''in simple words threading can be understood as an method to run more than 1 function at the same time without affecting the working of other'''
      
        thread=threading.Thread(target=handle_client, args=(client,))
        thread.start()

        print(f'Active connections: {threading.activeCount()-1}')       #to display no. of active connections
        print(usernames)
       
print("Server is ready")
print("This is the output of server side")
recieve()

