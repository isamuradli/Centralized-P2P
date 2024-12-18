Hi,

Project : Publish-Subscribe system

This project will support communication of 1 server and multiple clients.

Main Files in this project structure are server.py and client.py.
PingPong files are used for testing ping-pong test
myAPI.py holds all 5 different apis and registering the clients.
bashbenchmarkingAPI.sh is used to benchmark python file benchmarkAPI.py. It will trigger and run the specific api which user gives from prompt.

In this project to make its easy to work with, I suggest to use TMUX. It will enable us to open multiple panes in single teminal window

First please install tmux. To do so just do to the main folder of this project and run following:

1. make initial

Clients has access to 5 different APIs: {
CreateTopic(clientID, topic)
deleteTopic(clientID: int, topic: str)
send(clientID : int, topic : str, message : str)
subscribe(subID : int, topic : str)
pull(subID : int, topic : str)
}

topicID is randomly assinged when you create the client, so you dont need to worry about it.

After installing tmux (hopefully it worked for you :), we can get started.

1. Open the terminal in the main folder and type tmux
   After that tmux plugin will be open.

2. Now you can split the screen into to part.
   If you want to split vertically, please press Ctrl+B and after that press % (dont keep holding Ctrl B)
   If you want horizontally, please press Ctrl+B and after that press " (dont keep holding Ctrl B)

   To switch between panes, you can press Ctrl+B and use left, right, up, down arrow to navitage.
   Once you split the screen, now we can get started.

3. First we need to run server. If run client first, connection will be refused.

   You can run server by typing: make runServer
   Server will be waiting for the client to connect.

4. After you can run client by typing : make runClient
   After connecting, server will show IP and Port of the connection client

5. From client side you will see "Which function do you want to call?"
   There are 5 different functions to call. Last option is 5 or exit.
   You just need to choose from 0 to 5 according to what you want to do.

6. CreateTopic: First we start by creatingTopic which is 0. All of requests will be shown from server side, so that you can easily see what's going on.
   Once you type topic name, it gets added to the messageBuffer along with the clientID, which shows the ownership of the topic.
   Also the topic gets added to the subscriptions, so its available for others to subscribe to.

   Note: if you want to go back to main menu, you can text exit during using any API

7. Once topics are created, we can delete them, send messages to that topic.

8. DeleteTopic : To delete the topic, first type exit to quit the current menu option. After we type 1 which is option for deleteTopic
   Once we choose, we are asked to choose the topic to delete. You have to be the owner/creator of the topic to be able to delete it
   After we delete, server sends back us that "Topic has been deleted"
   If you try do delete topic that don't exist or you are not owner of, it will prompt that it doesnot exist for you

9. Send:
   To send message to topic, we choose option 2. Again, you have to be owner of the topic to send message.
   Once you choose Send, you are asked to specify the topic name to send message. If it exist, the message gets
   added to the messageBuffer of that topic.

10. Subscribe:
    You can also subscribe to other topics. To do so, let's open new pane in tmux. You can refer to 2nd point above to split the pane.
    In new page, run new client. From the options in the menu, you can choose 3 - Subscribe. After you get to specify the topic to subscribe.
    Once you subscribed, you can start pulling messages from there. Note: When you first subscribed to the topic, you readIndex is 0.
    Server will also send you the status message that you have been subscribed to the topic. If you try to resubscribe, it will say that you already
    subscribed to that topic.

11. Pull:
    Exit the subscribe menu by typing exit, and then choose option 4 - Pull.
    It will return all new messages that you have not read before. Be aware that once you read the message from a topic, those messages will not be readible again
    If you try to read again before the owner send message to that topic, you will get Empty message from the server

12. To close connection you can again type exit or just press Ctrl C 

NOTE: Do not shut down the server directly, first make sure you exit from the clients. And only after shut down the server. I will help not to corrupt the port


Benchmarking:
If you want to benchmark the APIs and see the number of requests handled by server, you will need open folder bash 1. To do so, type cd bash
Once you open that folder, you need to create the executable of the bash. 2. To do so please type: chmod +x bashBenchmarkAPI.sh

    After creating executable, you can get started.

    To call benchmark, you will need to specify the API name as well.
    Here how you will do it:
    3.    ./bashBenchmarkAPI.sh APINAME

    Please replace APINAME with one of these: benchmarkCreateTopic, benchmarkDeleteTopic, benchmarkSend, benchmarkSubscribe, benchmarkPull

    Client will start sending the requests to the server nonstop for 5 minutes and server will display the number of requests handled.

Ping-Pong:

    To do ping-pong between two clients A and B you can do following.
    1. In server.py file, uncomment lines from 18 - 30. I will populate 2 clients and 2 topics.
    2. Comment out lines 11,12,13 from server.py.
    3. Open the tmux and plit the pane into 2 (vertically - Ctrl B + %, horizontally Ctrl B + ")
    4. In one pane you run the server by calling makerunServer
    5. In other pane, run make runPingPong . It will open new 2 session and run the 2 clients at the same time in the background sessions.
    6. If you want to see background sessions of clients, press Ctrl B + S
    7. You will have overall 3 sessin: first_session, second_session and 1 windows which is main which we used to call the background clients
