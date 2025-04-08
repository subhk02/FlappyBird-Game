#!/bin/bash
if [[ $EUID -ne 0 ]]; then
    echo "Requesting sudo access to install packages..."
    sudo -v || exit 1
fi
sudo apt install -y python3 python3-venv python3-pip

cd ~/Documents
git clone https://github.com/subhk02/FlappyBird-Game.git
cd FlappyBird-Game
python3 -m venv venv
source venv/bin/activate
pip install pygame
chmod +x dflappy-bird.sh
./dflappy-bird.sh
