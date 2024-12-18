import threading
import socket
# from clientAPIs import subscribeAPI 
from clientAPIs import myAPI 

print('\Registering Client...\n')
clientID = myAPI.registerClient()

while True:
    try:
        answ = input("What function you want to call?\n0-createTopic\n1-deleteTopic\n2-sendMessage\n3-Subscribe\n4-Pull\n5-Exit\nOption: ")
        if int(answ) == 0:
            topicCreate = input("Enter topic to create -> ")
            myAPI.createTopic(clientID, topicCreate)
        if int(answ) == 1:
            topicDelete = input("\n Enter topic to delete-> ")
            myAPI.deleteTopic(clientID, topicDelete)
        if int(answ) == 2:
            topicToSendMessage = input("\n Which topic you want to send message ->")
            msgToSend = input("\nEnter message to send -> ")
            myAPI.send(clientID, topicToSendMessage, msgToSend)
        if int(answ) == 3:
            topicToSubscribe = input("Enter topic to subscribe -> ")
            myAPI.subscribe(clientID, topicToSubscribe)
        if int(answ) == 4:
            topicToPull = input("\n Enter topic to pull messages from -> ")
            myAPI.pull(clientID, topicToPull)
        elif  int(answ) ==5:
            myAPI.closeConnection()
            break
    except:
        myAPI.closeConnection()
        break