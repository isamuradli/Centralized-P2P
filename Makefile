runServer:
	python3 server/server.py 
	
runClient:
	python3 clients/client.py

install:
	sudo apt update
	sudo apt install tmux

runPingPong:
	chmod +x clients/bashPingPong.sh
	clients/bashPingPong.sh