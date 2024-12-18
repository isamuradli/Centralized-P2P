import sys
import socket
import random
import pickle
import string 
import time

host = socket.gethostname()
port = 5000
benchmarkSocket = socket.socket()
benchmarkSocket.connect((host,port))

clientID = 1
maxRequest = 0
numOfClients = 0


def benchmarkCreateTopic() -> None:
    
    #infinite loop for requests
    #start timer
    startTime = time.time()
    while True:
        timePassed = time.time() - startTime
        if timePassed >= 300:
            break
        #create random string name for topic
        topic = ''.join(random.choices(string.ascii_letters,k=4))
        msg = {'api':'benchmarkCreateTopic', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        benchmarkSocket.sendall(message) 
        #receive confirmation
        responseData = benchmarkSocket.recv(4096)
        responseData = pickle.loads(responseData)
        maxRequest = responseData['createTopicNumOfRequest']
        numOfClients = responseData['ConnectedClients']
        

        print(f'From server: {responseData}' )

    print(f"Maximum throughput for {numOfClients} is {maxRequest}")
    print("Closing benchmarkCreateTopic function...")
    return

def benchmarkDeleteTopic() -> None:
    startTime = time.time()
    #infinite loop for requests
    while True:
        timePassed = time.time() - startTime
        if timePassed >= 300:
            break
        #create random string name for topic
        topic = ''.join(random.choices(string.ascii_letters,k=4))
        msg = {'api':'benchmarkDeleteTopic', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        benchmarkSocket.sendall(message) 
        if topic =='exit':
            break
        #receive confirmation
        responseData = benchmarkSocket.recv(4096)
        responseData = pickle.loads(responseData)
        maxRequest = responseData['deleteTopicNumOfRequest']
        numOfClients = responseData['ConnectedClients']
        print(f'Received from server: {responseData}' ) 
        
    print(f"Maximum throughput for {numOfClients} is {maxRequest}")
    print("Closing benchmarkDeleteTopic function...")
    return

def benchmarkSend() -> None:
    startTime = time.time()
        #infinite loop for requests
    while True:
        timePassed = time.time() - startTime
        if timePassed >= 300:
            break
        #create random string name for topic
        message =  ''.join(random.choices(string.ascii_letters,k=4))
        msg = {'api' : 'benchmarkSend', 'client' : clientID, 'topic' : 'cs', 'message' : message}
        msg = pickle.dumps(msg)
        benchmarkSocket.sendall(msg)
        if not message or message == 'exit':
            break
        #receive confirmation
        responseData = benchmarkSocket.recv(4096)
        responseData = pickle.loads(responseData)
        maxRequest = responseData['SendNumOfRequest']
        numOfClients = responseData['ConnectedClients']
        print(f'Received from server: {responseData}' )

    print(f"Maximum throughput for {numOfClients} is {maxRequest}")
    print("Closing benchmarkDeleteTopic function...")
    return

def benchmarkSubscribe() -> None:
    startTime = time.time()
    #infinite loop for requests
    while True:
        timePassed = time.time() - startTime
        if timePassed >= 300:
            break
        #create random string name for topic
        topic = ''.join(random.choices(string.ascii_letters,k=4))
        msg = {'api':'benchmarkSubscribe', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        benchmarkSocket.sendall(message) 
        if topic == "exit":
            break
        
        #receive confirmation
        responseData = benchmarkSocket.recv(4096)
        responseData = pickle.loads(responseData)
        maxRequest = responseData['SubscribeNumOfRequest']
        numOfClients = responseData['ConnectedClients']
        print(f'From server: {responseData}' )

    print(f"Maximum throughput for {numOfClients} is {maxRequest}")
    print("Closing benchmarkSubscribe function...")
    return

def benchmarkPull() -> None:
    startTime = time.time()
    #infinite loop for requests
    while True:
        timePassed = time.time() - startTime
        if timePassed >= 300:
            break
          #create random string name for topic
        topic = 'cs'
        msg = {'api':'benchmarkPull', 'client':clientID, 'topic':topic}
        message = pickle.dumps(msg)
        benchmarkSocket.sendall(message) 
        if topic =='exit':
            break
        #receive confirmation
        responseData = benchmarkSocket.recv(4096)
        responseData = pickle.loads(responseData)
        maxRequest = responseData['PullNumOfRequest']
        numOfClients = responseData['ConnectedClients']
        print(f'Received from server: {responseData}' ) 

    print(f"Maximum throughput for {numOfClients} is {maxRequest}")


    print("Closing benchmarkPull function...")
    return

def closeConnection():
    benchmarkSocket.close()  
    print("Closed connection")
    return # close the connection

if __name__ == '__main__':
        #check which API is called from the input arguments
    if len(sys.argv) > 1:
        apiName = sys.argv[1]
        if apiName =="benchmarkCreateTopic":
            benchmarkCreateTopic()
        if apiName =="benchmarkDeleteTopic":
            benchmarkDeleteTopic()
        if apiName =="benchmarkSend":
            benchmarkSend()
        if apiName =="benchmarkSubscribe":
            benchmarkSubscribe()
        if apiName =="benchmarkPull":
            benchmarkPull()