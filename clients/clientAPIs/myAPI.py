import socket
import random
import pickle
import string 

#setting up the connectiong
host = socket.gethostname()
port = 5000
clientSocket = socket.socket()

#randomly assing a number to client
def registerClient(*args):
    clientSocket.connect((host,port))
    if not args:
        clientID = random.randint(0, 1000)
    else:
        clientID = args[0]
    print(f"\nClient ID: {clientID}")
    return clientID
    

def createTopic(clientID: int, topic: str) -> None:
    #check that topic is not exit
    while topic.lower() != "exit":
        #serialize the package
        msg = {'api':'createTopic', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        clientSocket.sendall(message) 
        if topic == "exit":
            break
        #receive confirmation
        responseData = clientSocket.recv(4096)
        responseData = pickle.loads(responseData)
        print(f'Received from server: {responseData}' ) 

        topic = input("Enter topic to create-> ")  

        
def deleteTopic(clientID: int, topic: str) -> None:
    #check that topic is not exit   
    while topic.lower() != 'exit':
         #serialize the package
        msg = {'api':'deleteTopic', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        clientSocket.sendall(message) 

        #receive confirmation
        responseData = clientSocket.recv(4096)
        responseData = pickle.loads(responseData)
        print(f'Received from server: {responseData}' ) 

        topic = input("Enter topic to delete-> ")  

    return

def send(clientID : int, topic : str, message : str) -> None:
    while message.lower().strip() != "exit":
         #serialize the package
        msg = {'api' : 'send', 'client' : clientID, 'topic' : topic, 'message' : message}
        msg = pickle.dumps(msg)
        clientSocket.sendall(msg)

        #receive confirmation
        responseData = clientSocket.recv(4096)
        responseData = pickle.loads(responseData)
        print(f"Received from server: {responseData}")

        message = input(f"Enter message to send-> ")
    print("Closing Send functions")
    return

def sendPingPong(clientID : int, topic : str, message : str) -> None:
    while message.lower().strip() != "exit":
         #serialize the package
        msg = {'api' : 'send', 'client' : clientID, 'topic' : topic, 'message' : message}
        msg = pickle.dumps(msg)
        clientSocket.sendall(msg)

        #receive confirmation
        responseData = clientSocket.recv(10240)
        responseData = pickle.loads(responseData)
        print(f"Received from server: {responseData}")

        # message = input(f"Enter message to send-> ")
        # ---- for ping pong --------#
        message = 'exit'
    return

def subscribe(subID : int, topic : str) -> None:
    #check the topic name 
    while topic.lower() != 'exit':
        #serialize the parameters
        msg = {'api':'subscribe', 'client' : subID, 'topic':topic}
        message = pickle.dumps(msg)
        clientSocket.sendall(message)
        if topic == 'exit':
            break
        
        responseData = clientSocket.recv(4096)
        responseData = pickle.loads(responseData)
        print(f"Received from server: {responseData}")

        topic = input("Enter topic to subscribe -> ")

def pull(subID : int, topic : str) -> None:
    #check topic if its exit
    while topic.lower() != 'exit':
         #serialize the package
        msg = {'api':'pull', 'client' : subID, 'topic':topic}
        message = pickle.dumps(msg)
        clientSocket.sendall(message)
        if topic == 'exit':
            break
        
        responseData = clientSocket.recv(4096)
        responseData = pickle.loads(responseData)
        print(f"Received from server: {responseData}")

        topic = input("Enter topic to pull -> ")
    

def pullPingPong(subID : int, topic : str) -> None:
    #check topic if its exit
    while topic.lower() != 'exit':
         #serialize the package
        msg = {'api':'pull', 'client' : subID, 'topic':topic}
        message = pickle.dumps(msg)
        clientSocket.sendall(message)
        if topic == 'exit':
            break
        
        responseData = clientSocket.recv(10240)
        responseData = pickle.loads(responseData)
        print(f"Received from server: {responseData}")

        # topic = input("Enter topic to pull -> ")
        # ---- for ping pong --------#
        topic = 'exit'
    
    
#close connection once done
def closeConnection():
    clientSocket.close()  
    print("Closed connection")
    return # close the connection