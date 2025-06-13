# Othello (Reversi) Game with Minimax AI

## 🎮 Overview

This project is a **Python-based Othello (Reversi) game** featuring a graphical user interface (GUI) built with **Pygame** and an AI opponent powered by the **Minimax algorithm**. The AI simulates future moves to make intelligent decisions and provides a challenging opponent for the player.

---

## 🧩 Features

- Fully playable Othello game against the computer
- Graphical game board rendered with **Pygame**
- Computer opponent uses the **Minimax algorithm** to decide optimal moves
- Interactive and intuitive GUI
- Adjustable AI search depth (if implemented)
- Clear and well-structured Python code

---

## 🔧 Requirements

- Python 3.x
- Pygame library

You can install Pygame via pip:

```bash
pip install pygame
```

## 🚀 How to Run

1. Clone this repository or download the source code:
   
```bash
git clone https://github.com/milanlazarevic/OthelloGame.git
```

3. Run the main Python file:

```bash
python3 main.py
```

## Adjust the bot dificulty

In the computer.py in Computer class adjust **MAX_DEPTH** and **MAX_TIME** properties

**MAX_DEPTH** is the maximum recursion depth of the minimax algorithm. By default set to **5**
**MAX_TIME** is the maximum time after which recursion will stop and return current best move. By default set to **1s**


## App screenshots

1. Game start
   
   ![Screenshot from 2025-06-13 20-50-51](https://github.com/user-attachments/assets/3f34078f-c1aa-49f3-b271-c2c9397b6a8b)

2. Gameplay

   ![Screenshot from 2025-06-13 20-51-37](https://github.com/user-attachments/assets/45b7b57c-2f84-4f12-90c0-fa1abf957522)







