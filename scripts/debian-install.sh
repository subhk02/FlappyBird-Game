#!/bin/bash
cd ~/Documents
sudo apt install python3 python3-venv python3-pip
git clone https://github.com/subhk02/FlappyBird-Game.git
cd FlappyBird-Game
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x flappy-bird.sh
./flappy-bird.sh