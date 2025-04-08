#!/bin/bash
if [[ $EUID -ne 0 ]]; then
    echo "Requesting sudo access to install packages..."
    sudo -v || exit 1
fi
sudo pacman -S --noconfirm python python-virtualenv python-pip

cd ~/Documents
git clone https://github.com/subhk02/FlappyBird-Game.git
cd FlappyBird-Game
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x flappy-bird.sh
./flappy-bird.sh