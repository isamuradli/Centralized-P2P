import socket 
import threading
import pickle
import _thread
import random
import string

class Server():
    def __init__(self) -> None:
        self.connectedClients = 0 #used for benchmarking
        self.messageBuffer = {}  # holds (topic, ownerID) : [messages]
        self.subscriptions = {}  # holds topic : [sub1, sub2]
        self.readHistory = {}    # holds (topic, subID) : index
        self.grbCollectIndex = 0    #used to keep track of the index of the clients to check garbage collector 


        #------- PING PONG  ---------#
        # self.messageBuffer ={
        #     ('topicOfA',1) : ['MessageOfA'],
        #     ('topicOfB',2) : ['MessageOfB']
            
        # }
        # self.subscriptions = {
        #     'topicOfA' : [2],
        #     'topicOfB' : [1]
        # }
        # self.readHistory = {
        #     ('topicOfA',2) : 0,
        #     ('topicOfB',1) : 0
        # }

        
        self.createTopicBenchmark = 0  #used to benchmark CreateTopic API
        self.deleteTopicBenchmark = 0   #used to benchmark DeleteTopic API
        self.sendBenchmark = 0 #used to benchmark Send API
        self.pullBenchmark = 0  #used to benchmark Pull API
        self.subscribeBenchmark = 0  #used to benchmark Pull API
        self.sendPingPong = 0
        self.pullPingPong = 0
        self.host = socket.gethostname()    #host
        self.port = 5000   #port
        

        # this part used only during benchmarkDeleteTopic/benchmarkSend
        # for i in range(1000000):
        #     topic = ''.join(random.choices(string.ascii_letters,k=4))
        #     self.messageBuffer[(topic, 1)] = []
        #     self.subscriptions[topic] = []

        # #used for Pull benchmarking
        # for i in range(1000000):
        #     message = ''.join(random.choices(string.ascii_letters,k=4))
        #     self.messageBuffer[('cs', 1)].append(message)

    def execute(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM - TCP
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # solution for "[Error 89] Address already in use". Use before bind()  
        serverSocket.bind((self.host,self.port)) #binding IP and Host 
        serverSocket.listen(2)  #Opens connection and listen for incoming conns
        try:
            while True:
                print("Waiting for client...")
                conn, addr = serverSocket.accept() #accepts the connection
                myThread=threading.Thread(target=self.handleClient, args = (conn, addr))    #Calls the thread for the client who connected to server
                myThread.start() 
                self.connectedClients +=1

        except KeyboardInterrupt:
            print("Stopped by Ctrl-C")
        finally:
            if serverSocket:
                serverSocket.close()
        serverSocket.close()

    def garbageCollector(self, topic, ownerID, key):
        #check if everyone read the messages
        self.grbCollectIndex = len(self.messageBuffer[(topic,ownerID)])

        for key in self.readHistory.keys():
            #pick up the same topic
            if key[0] == topic and self.grbCollectIndex != 0:
                self.grbCollectIndex = min(self.grbCollectIndex, self.readHistory[key])
                                    

        if self.grbCollectIndex == len(self.messageBuffer[(topic,ownerID)]) and len(self.messageBuffer[(topic,ownerID)]) !=0:
            self.messageBuffer[(topic,ownerID)] = []    #garbage collect 
            #set all indexes to 0 after garbage collected
            for key in self.readHistory.keys():
                if key[0] == topic:
                    self.readHistory[key] = 0
            print(f"Garbage collected!")


    #handles all incoming APIs
    def handleClient(self, connection, address):
        print(f"\nInside handle function: \nConnection from : {address}")
        try:
            while True:
                #receives data of size 4096
                data = connection.recv(4096)
                if not data:
                    break
                
                #Deserialize the message from client
                dataObject = pickle.loads(data)
                print(f"Request from connected user: {dataObject}" )

                #Deserialize
                apiName, clientID, topic = dataObject['api'], dataObject['client'], dataObject['topic']

                #check which API is that


                #handle CreateTopic
                if apiName == 'createTopic':
                    #check if topic in the messageBuffer
                    checkForTopic = False 
                    for key in self.messageBuffer.keys():
                        if key[0] == topic:
                            checkForTopic = True
                            break
                    #If topic missing then adds topic and ownerID to buffer.
                    if (topic, clientID) not in self.messageBuffer.keys() and checkForTopic == False:
                        self.messageBuffer[(topic, clientID)] = [] #when created, there is empty messages
                        self.subscriptions[topic] = []  #no subs exist when topic just created.
                        reply = {'status':'Topic added'}
                    else:  
                        reply = {'status': 'Failed. Topic already exists'}
        
                #handle DeleteTopic
                if apiName == 'deleteTopic':
                    #check if topic and calling client exists
                    if (topic, clientID) in self.messageBuffer.keys():
                        del self.messageBuffer[(topic,clientID)] 
                        del self.subscriptions[topic]
                    #delete all clients that were subscribed to that topic.
                        readingHistory = []
                        for i in self.readHistory.keys():
                            readingHistory.append((i[0],i[1]))
                        
                        for i in readingHistory:
                            del self.readHistory[i]

                        reply = {'status':'Topic has been deleted!'}
                    else:
                        #Calling client does not have that topic
                        reply = {'status': 'Failed. Your topic does not exist.'}

                #handle sendMessage
                if apiName == 'send':
                    #deserialize the message
                    message = dataObject['message']
                    #check if topic and clientID exist in the buffer
                    if (topic,clientID) in self.messageBuffer and message:
                        self.messageBuffer[(topic,clientID)].append(message)
                        reply = {'status':'Message added!'}
                    elif (topic,clientID) not in self.messageBuffer:
                        reply = {'status':f'Topic {topic} for {clientID} does not exist'}
                    elif not message:
                        reply = {'status' : 'Empty message'}
                    
                    self.sendPingPong +=1
                    
                #handle Subscriptions
                if apiName == 'subscribe':
                    #check if topic exist in buffer
                    topicExist = False
                    for key in self.messageBuffer.keys():
                        if key[0] == topic:
                            topicExist = True
                            break
                    if topicExist:
                        #check if client subscribed to topic or not
                        if clientID not in self.subscriptions[topic]:
                            self.subscriptions[topic].append(clientID)
                            self.readHistory[(topic,clientID)] = 0     # when subscribed, we initialize the index to 0
                            reply = {'status' : f" Client {clientID} subscribed to {topic}. Great!"}
                        else:
                            reply = {'status' : f"{clientID} already subscribed to the topic {topic}"}
                    else:
                        reply = {'status' : f"{topic} does not exist "}
                    
                #handle benchmarking CreateTopic - prototype of actual API.
                if apiName =='benchmarkCreateTopic':
                    #once received, increment the counter by 1
                    self.createTopicBenchmark+=1
                    checkForTopic = False
                    for key in self.messageBuffer.keys():
                        if key[0] == topic:
                            checkForTopic = True
                            break
                    if (topic, clientID) not in self.messageBuffer.keys() and checkForTopic == False:
                        self.messageBuffer[(topic, clientID)] = []
                        self.subscriptions[topic] = []
                        reply = {'status':'Topic added'}
                    else:  
                        reply = {'status': 'Failed. Topic already exists'}
                    
                    reply = {'createTopicNumOfRequest' : self.createTopicBenchmark,
                             'sizeOfMessageBuffer' : len(self.messageBuffer),
                             'ConnectedClients' : self.connectedClients}
                
                #handle benchmarking DeleteTopic
                if apiName =='benchmarkDeleteTopic':
                    #once received, increment the counter by 1
                    self.deleteTopicBenchmark+=1
                    print('Checking!!')
                    if (topic, clientID) in self.messageBuffer.keys():
                        del self.messageBuffer[(topic,clientID)] 
                        print('Deleted!!')
                        del self.subscriptions[topic]
                        #when topic is delete, we delete all subscribed users. 
                        readingHistory = []
                        for i in self.readHistory.keys():
                            readingHistory.append((i[0],i[1]))
                        
                        for i in readingHistory:
                            del self.readHistory[i]

                        reply = {'status':'Topic has been deleted!'}
                    else:
                        reply = {'status': 'Failed. Your topic does not exist.'}

                    reply = {'deleteTopicNumOfRequest' : self.deleteTopicBenchmark,
                             'sizeOfMessageBuffer' : len(self.messageBuffer),
                             'ConnectedClients' : self.connectedClients}

                #handle benchmarking Send
                if apiName =='benchmarkSend':
                    self.sendBenchmark +=1
                    message = dataObject['message']
                    if (topic,clientID) in self.messageBuffer and message:
                        self.messageBuffer[(topic,clientID)].append(message)
                        reply = {'status':'Message added!'}
                    elif (topic,clientID) not in self.messageBuffer:
                        reply = {'status':f'Topic {topic} for {clientID} does not exist'}
                    elif not message:
                        reply = {'status' : 'Empty message'}

                    reply = {'SendNumOfRequest' : self.sendBenchmark,
                            'ConnectedClients' : self.connectedClients}

                #handle benchmarking Subscribe
                if apiName =='benchmarkSubscribe':
                    self.subscribeBenchmark +=1
                    topicExist = False
                    for key in self.messageBuffer.keys():
                        if key[0] == topic:
                            topicExist = True
                            break
                    if topicExist:
                        if clientID not in self.subscriptions[topic]:
                            self.subscriptions[topic].append(clientID)
                            self.readHistory[(topic,clientID)] = 0     # when subscribed, we initialize the index to 0
                            reply = {'status' : f" Client {clientID} subscribed to {topic}. Great!"}
                            print('Subscribed!\n')
                        else:
                            reply = {'status' : f"{clientID} already subscribed to the topic {topic}"}
                    else:
                        reply = {'status' : f"{topic} does not exist "}


                    reply = {'SubscribeNumOfRequest' : self.subscribeBenchmark,
                            'ConnectedClients' : self.connectedClients}
                    
                if apiName =='benchmarkPull':
                    self.pullBenchmark +=1
                    #check if topic exist to pull from
                    topicExist = False
                    for key in self.messageBuffer.keys():
                        if key[0] == topic:
                            topicExist = True
                            ownerID = key[1]
                            break
                    if topicExist == True:
                        # check if client subscribed:
                        if clientID not in self.subscriptions[topic]:
                            reply = {'message' : f'Client {clientID} not subscribed to topic {topic}'}
                        else:
                            #getting last index the client has read before 
                            indexToStart = self.readHistory[(topic, clientID)]
                            #check if buffer has new message -> size is more that index of the subscriber
                            if len(self.messageBuffer[(topic,ownerID)]) > indexToStart and len(self.messageBuffer[(topic,ownerID)]) != 0:
                                print(self.messageBuffer[(topic,ownerID)][indexToStart::])
                                reply = {'Message' : self.messageBuffer[(topic,ownerID)][indexToStart::]}
                                lastIndexRead = len(self.messageBuffer[(topic,ownerID)])
                                self.readHistory[(topic, clientID)] = lastIndexRead
                            elif len(self.messageBuffer[(topic,ownerID)]) == indexToStart or len(self.messageBuffer[(topic,ownerID)]) == 0:
                                reply = {'status' : 'Empty'}
                            #check if everyone read the messages
                            self.grbCollectIndex = len(self.messageBuffer[(topic,ownerID)])
                            for key in self.readHistory.keys():
                                #pick up the same topic
                                if key[0] == topic and self.grbCollectIndex != 0:
                                    self.grbCollectIndex = min(self.grbCollectIndex, self.readHistory[key])
                                
                            if self.grbCollectIndex == len(self.messageBuffer[(topic,ownerID)]) and len(self.messageBuffer[(topic,ownerID)]) !=0:
                                self.messageBuffer[(topic,ownerID)] = []    #garbage collect 
                                #set all indexes to 0 after garbage collected
                                for key in self.readHistory.keys():
                                    if key[0] == topic:
                                        self.readHistory[key] = 0
                    else:
                        reply = {'message' : f'Topic {topic} does not exist!'}


                    reply = {'PullNumOfRequest' : self.pullBenchmark,
                            'ConnectedClients' : self.connectedClients}
                #handle Pull
                try:
                    if apiName == 'pull':
                        
                        #check if topic exist to pull from
                        topicExist = False
                        for key in self.messageBuffer.keys():
                            if key[0] == topic:
                                topicExist = True
                                ownerID = key[1]
                                break
                        
                        if topicExist == True:

                            # check if client subscribed:
                            if clientID not in self.subscriptions[topic]:
                                reply = {'message' : f'Client {clientID} not subscribed to topic {topic}'}
                            else:
                                #getting last index the client has read before 
                                indexToStart = self.readHistory[(topic, clientID)]


                                #check if buffer has new message -> size is more that index of the subscriber
                                if len(self.messageBuffer[(topic,ownerID)]) > indexToStart and len(self.messageBuffer[(topic,ownerID)]) != 0:
                                    print(self.messageBuffer[(topic,ownerID)][indexToStart::])
                                    reply = {'Message' : self.messageBuffer[(topic,ownerID)][indexToStart::]}
                                    lastIndexRead = len(self.messageBuffer[(topic,ownerID)])
                                    self.readHistory[(topic, clientID)] = lastIndexRead
                                elif len(self.messageBuffer[(topic,ownerID)]) == indexToStart or len(self.messageBuffer[(topic,ownerID)]) == 0:
                                    reply = {'status' : 'Empty'}

                                #call garbage collector after each pull                                    
                                self.garbageCollector(topic, ownerID, key)
                                
                        else:
                            reply = {'message' : f'Topic {topic} does not exist!'}
                        
                    self.pullPingPong +=1
                        
                    #Print out Message Buffer and Subscriptions
                    if self.messageBuffer :
                        print(f"\nMessageBuffers are {self.messageBuffer}\n")
                    else:
                        print(f"No topic in the system")
                    self
                    if self.subscriptions :
                        print(f"Subscriptions are {self.subscriptions}\n")
                    else:
                        print(f"No subscription in the system")
                                      

                    #Sending the confirmation
                    
                    replyData = pickle.dumps(reply)
                    connection.sendall(replyData)
                except KeyError as k:
                    pass
                    return
        except OSError as e:
            print(f"Error is {e}")
        finally:
            print("--------- Used for benchmarking -----------")
            print(f"\nNumber of Pull for {self.connectedClients} is {self.pullPingPong}")
            print(f"Number of Sends for {self.connectedClients} is {self.sendPingPong}\n")
            #remove client when he disconnects
            for tpc in self.subscriptions:
                if clientID in self.subscriptions[tpc]:
                    self.subscriptions[tpc].remove(clientID)

            #delete client indexes of messages.
            if self.readHistory:
                for key in self.readHistory.keys():
                    if key[1] == clientID:
                        del self.readHistory[key]
            
            print("Closing connection ..")
            connection.close()   
            exit()
            


#close the threads as well


server = Server()
server.execute()