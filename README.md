
# Two Flags Game AI Module:

## Overview
The **`enpassant`** module is a core component of the **Two Flags Game**, responsible for **AI decision-making, game state evaluation, and networking functionalities**. It includes an **AI engine**, **evaluation functions**, a **game timer**, and **networking components** to enable both local and online play.

## Key Features
- **AI-Based Decision Making**: Implements an **AI engine** using a variation of the **Nega-MinMax** algorithm.
- **Game State Evaluation**: Uses an **evaluation function** to assess board positions.
- **Zobrist Hashing**: Utilizes **transposition tables** for efficient state storage and retrieval.
- **Multithreading Support**: Uses **process queues** to optimize AI computations.
- **Networking Support**: Implements **client-server communication** for multiplayer games.

## Directory Structure
```
enpassant/
├── AI.py                 # Implements the AI decision-making algorithm
├── Client.py             # Handles client-side networking functionality
├── Server.py             # Manages server-side communication for network play
├── enpassant_engine.py   # Handles game state representation and updates
├── enpassant_main.py     # Main entry point for executing the game
├── evaluation.py         # Evaluates board positions and assigns scores
├── settings.py           # Stores game settings and board configurations
├── timer.py              # Implements in-game countdown timers
├── transposition.py      # Zobrist hashing and transposition table management
├── images/               # Contains graphical assets for the game
│   ├── bp.png            # Black pawn image
│   ├── wp.png            # White pawn image
```

## How the Module Works

### 1. AI Decision-Making (`AI.py`)
- Implements **Nega-MinMax with Alpha-Beta pruning** to determine the best move.
- Uses **transposition tables** to speed up repetitive calculations.
- Stores AI-evaluated board states in **hash tables** (`HashTableforPlayer1` and `HashTableforPlayer2`).

#### Example AI Execution Flow
```python
from AI import ai
from enpassant_engine import GameState

game_state = GameState()
best_move = ai(game_state, valid_moves, move_values, depth=3, Queue=None)
print(f"Best move determined by AI: {best_move}")
```

### 2. Game State Representation (`enpassant_engine.py`)
- Stores the **current board position**, **history of moves**, and **active game state**.
- Uses **bitwise operations** for fast move generation.
- Supports **undo functionality** by maintaining a history stack.

### 3. Game Evaluation (`evaluation.py`)
- Assigns numerical scores to different board positions.
- Considers factors such as:
  - **Threatened pieces**
  - **Safe positions**
  - **Winning or losing conditions**

### 4. Zobrist Hashing & Transposition Tables (`transposition.py`)
- Uses **Zobrist Hashing** to uniquely identify board positions.
- Prevents AI from **recomputing previously seen positions**.

### 5. Timer & Game Control (`timer.py`)
- Implements **a countdown clock** for each player.
- Uses **Pygame fonts** to render the timer on-screen.

### 6. Networking (`Client.py` & `Server.py`)
- **Client (`Client.py`)**:
  - Connects to the game server.
  - Handles sending and receiving move data.

- **Server (`Server.py`)**:
  - Hosts the game.
  - Uses **multi-threading** to handle multiple connections.

## How to Run the Module

### 1. Local Play (AI vs AI / AI vs Human)
```bash
python enpassant_main.py
```

### 2. Multiplayer Mode (Network Play)
#### Start the Server
```bash
python server.py
```
#### Connect as a Client
```bash
python Client.py --connect --ip 127.0.0.1
```

## Key Takeaways
✅ **AI-powered game engine** with advanced decision-making  
✅ **Bitwise board representation** for optimized performance  
✅ **Zobrist hashing** to reduce redundant calculations  
✅ **Networking capabilities** for multiplayer mode  
✅ **Configurable evaluation functions** to adjust AI difficulty  

## Future Improvements
🚀 **Quiescence Search**: Enhance AI decision-making by analyzing only critical moves.  
🚀 **Parallelized AI Computation**: Speed up move evaluations using multiprocessing.  
🚀 **Improved Threat Analysis**: Implement more advanced heuristics for evaluating board threats.  

---
GUI :
![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/7408989f-e56a-48fb-a0ce-b04fd0a53c7d)


![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/8d00eae2-a8c5-4294-b37b-65f3efe0e122)


![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/b03ccc7d-f6e4-4794-be00-d31a24fd093a)



