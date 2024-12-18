tmux new-session -d -s first_session
tmux new-session -d -s second_session


tmux send-keys -t first_session:0 "python3 PingPongclientA.py" C-m
tmux send-keys -t second_session:0 "python3 PingPongclientB.py" C-m