# 🐦 Flappy Bird Game

A simple and fun Flappy Bird clone built with Python and Pygame.

## ⚡ Automatic Install (One-liner Script)

Skip the manual steps! Use one of the following one-liner install scripts based on your OS:

### 🧩 For Debian-based users
#### 🐚 Bash Users
```sh
bash <(curl -L https://raw.githubusercontent.com/subhk02/FlappyBird-Game/main/scripts/debian-install.sh)
```
#### 🐟 FIsh Users
```sh
curl -L https://raw.githubusercontent.com/subhk02/FlappyBird-Game/main/scripts/debian-install.sh | sh
```

### 🐧 For Arch Linux users
#### 🐚 Bash Users
```sh
sh <(curl -l https://raw.githubusercontent.com/subhk02/FlappyBird-Game/main/scripts/arch-install.sh)
```
#### 🐟 FIsh Users
```sh
curl -L https://raw.githubusercontent.com/subhk02/FlappyBird-Game/main/scripts/arch-install.sh | sh
```

## 🚀 Installation & Setup

1. **Install Python** (if you haven't already).  
   [Download from python.org](https://www.python.org/downloads/)

2. **Only for Debian users** Run this command in your main terminal
   ```sh
   sudo apt update
   sudo apt install python3 python3-venv python3-pip 
   ```

3. **Clone the repository**:
   ```sh
   git clone https://github.com/subhk02/FlappyBird-Game.git
   cd FlappyBird-Game
   ```

4. Open the folder `FlappyBird-Game` and open a terminal inside it.

5. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

6. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

7. **Run the game**:
   ```sh
   chmod +x flappy-bird.sh
   ./flappy-bird.sh
   ```
## 🎮 How to Play

- **Press the spacebar** to flap and keep the bird flying
- **Avoid hitting the pipes!**
