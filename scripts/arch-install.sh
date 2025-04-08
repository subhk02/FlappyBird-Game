#!/bin/bash
cd ~/Downloads
pacman install python python-venv python-pip
git clone https://github.com/subhk02/FlappyBird-Game.git
cd FlappyBird-Game
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x flappy-bird.sh
./flappy-bird.sh