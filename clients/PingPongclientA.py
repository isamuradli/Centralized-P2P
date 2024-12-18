import threading
import socket
# from clientAPIs import subscribeAPI 
from clientAPIs import myAPI 
import random
import string
import time

clientID = myAPI.registerClient(1)
startTime = time.time()
while True:
    timePassed = time.time() - startTime
    if timePassed >= 10:
        break
    msg = topic = ''.join(random.choices(string.ascii_letters,k=5))
    myAPI.sendPingPong(clientID,"topicOfA", msg)
    myAPI.pullPingPong(clientID, "topicOfB")