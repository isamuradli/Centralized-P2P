import threading
import socket
from clientAPIs import myAPI 
import random
import string
import time

clientID = myAPI.registerClient(2)

startTime = time.time()
while True:
    timePassed = time.time() - startTime
    if timePassed >= 300:
        break
    msg = topic = ''.join(random.choices(string.ascii_letters,k=5))
    myAPI.sendPingPong(clientID,"topicOfB", msg)
    myAPI.pullPingPong(clientID, "topicOfA")