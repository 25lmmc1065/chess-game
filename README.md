# Chess Game - Player vs AI / शतरंज खेल - खिलाड़ी बनाम AI

A complete chess game implementation in Python featuring a powerful AI opponent using Minimax algorithm with Alpha-Beta pruning. Available in both **GUI** and **CLI** modes.

![Chess Game GUI](https://github.com/user-attachments/assets/7f898f97-d555-4a50-bf40-3227f33e8cd3)

## Features / विशेषताएं

### Core Features:
- **Player vs AI Mode**: Play against a strong AI opponent
- **Choice of First Move**: Choose to play as White or Black
- **Strong AI Implementation**:
  - Minimax algorithm with Alpha-Beta pruning
  - Advanced evaluation function considering material, position, and mobility
  - Search depth of 3 plies (configurable in code) for strong gameplay
- **Two Interface Options**:
  - **GUI Mode** (Recommended): Beautiful graphical interface with clearly distinguishable piece shapes
  - **CLI Mode**: ASCII board display for terminal use
- **Hindi Language Support**: Bilingual prompts and messages

### Additional Features:
- Display of captured pieces
- Move history tracking
- Legal move highlighting (GUI)
- Last move highlighting (GUI)
- Check indication
- Support for both UCI (e.g., e2e4) and SAN (e.g., Nf3) notation (CLI)
- Resignation option
- Complete game state detection (checkmate, stalemate, draw)

## Requirements / आवश्यकताएं

- Python 3.7 or higher
- python-chess library
- pygame library (for GUI mode)

## Installation / स्थापना

1. Clone the repository:
```bash
git clone https://github.com/25lmmc1065/chess-game.git
cd chess-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run / कैसे चलाएं

### GUI Mode (Recommended) / ग्राफिकल मोड
Run the graphical version with beautiful piece graphics:
```bash
python chess_game_gui.py
```

### CLI Mode / कमांड लाइन मोड
Run the command-line version:
```bash
python chess_game.py
```

## How to Play / कैसे खेलें

### GUI Mode:
1. **Start the Game**: Run `python chess_game_gui.py`
2. **Choose Color**: Click on White or Black button to select your color
3. **Make Moves**: 
   - Click on a piece to select it (legal moves will be highlighted)
   - Click on a highlighted square to move the piece
4. **Special Actions**:
   - Click "New Game" to start a new game
   - Click "Resign" to resign the current game
5. **Win the Game**: Checkmate your opponent or force a draw

### CLI Mode:
1. **Start the Game**: Run `python chess_game.py`
2. **Choose Color**: Select whether you want to play as White (first) or Black (second)
3. **Make Moves**: 
   - Enter moves in UCI format (e.g., `e2e4` to move pawn from e2 to e4)
   - Or use SAN notation (e.g., `Nf3` for knight to f3)
   - You have 15 seconds to make each move
4. **Special Commands**:
   - Type `history` to view all moves played so far
   - Type `resign` to concede the game
5. **Win the Game**: Checkmate your opponent or force a draw

## Chess Pieces / शतरंज के मोहरे

Each piece has a distinctive shape that makes it easy to identify:

| Piece | Name (English/Hindi) | Shape Description |
|-------|---------------------|-------------------|
| ♔/♚ | King / राजा | Cross on top |
| ♕/♛ | Queen / रानी | Crown with 5 points and balls |
| ♖/♜ | Rook / हाथी | Castle with battlements |
| ♗/♝ | Bishop / ऊंट | Pointed miter (hat) |
| ♘/♞ | Knight / घोड़ा | Horse head |
| ♙/♟ | Pawn / प्यादा | Simple rounded shape |

## Game Interface Example

```
Welcome to Chess Game! / शतरंज के खेल में आपका स्वागत है!
==================================================

Choose who plays first / चुनें कौन पहले खेलेगा:
1. User (White) / उपयोगकर्ता (सफेद)
2. AI (White) / AI (सफेद)

Enter choice (1/2) / विकल्प दर्ज करें (1/2): 1

  a b c d e f g h
8 r n b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 P P P P P P P P
1 R N B Q K B N R

Your turn (White) / आपकी बारी (सफेद)
Time remaining: 15 seconds / शेष समय: 15 सेकंड
Enter move (e.g., e2e4) / चाल दर्ज करें: e2e4
```

## AI Algorithm Details

### Minimax with Alpha-Beta Pruning
The AI uses the Minimax algorithm with Alpha-Beta pruning to search the game tree efficiently:
- **Search Depth**: 3 plies by default (can be changed by modifying `self.search_depth` in the code)
- **Alpha-Beta Pruning**: Eliminates unnecessary branches to speed up search
- **Move Ordering**: Prioritizes captures for better pruning

### Evaluation Function
The AI evaluates positions based on:
- **Material Value**: 
  - Pawn = 100
  - Knight = 320
  - Bishop = 330
  - Rook = 500
  - Queen = 900
  - King = 20000
- **Piece-Square Tables**: Positional bonuses for optimal piece placement
- **Mobility**: Bonus for having more legal moves
- **King Safety**: Different tables for middlegame and endgame

## Move Notation

### UCI Format (Universal Chess Interface)
- Format: `[from_square][to_square]`
- Examples:
  - `e2e4` - Move piece from e2 to e4
  - `g1f3` - Move piece from g1 to f3
  - `e7e8q` - Pawn promotion to queen

### SAN Format (Standard Algebraic Notation)
- Examples:
  - `e4` - Pawn to e4
  - `Nf3` - Knight to f3
  - `O-O` - Kingside castling
  - `O-O-O` - Queenside castling
  - `Qxd5` - Queen captures on d5

## Game End Conditions

The game ends when:
- **Checkmate**: One king is in check and cannot escape
- **Stalemate**: Player has no legal moves but is not in check
- **Insufficient Material**: Not enough pieces to checkmate
- **Resignation**: A player types 'resign'
- **Timeout**: A player runs out of time
- **Draw by Repetition**: Position repeats 5 times
- **75-Move Rule**: 75 moves without capture or pawn move

## Project Structure

```
chess-game/
├── chess_game_gui.py  # GUI version with graphical pieces
├── chess_game.py      # CLI version with ASCII board
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Technical Implementation

### Libraries Used
- **python-chess**: Handles chess rules, move validation, and game state
- **pygame**: Provides graphical interface and piece rendering (GUI mode)
- **threading**: Implements move timer functionality (CLI mode)
- **time**: Time tracking for AI thinking

### Key Classes and Functions

#### GUI Version (`chess_game_gui.py`):
- `PieceRenderer`: Renders distinct graphical chess pieces
- `ChessGameGUI`: Main game class with graphical interface
  - `draw_board()`: Draws the chess board with highlights
  - `draw_pieces()`: Renders pieces using distinct shapes
  - `minimax()`: AI move selection using Minimax with Alpha-Beta pruning
  - `handle_click()`: Processes mouse clicks for piece selection and movement

#### CLI Version (`chess_game.py`):
- `ChessGame`: Main game class
  - `evaluate_position()`: Evaluates board positions
  - `minimax()`: AI move selection using Minimax with Alpha-Beta pruning
  - `get_ai_move()`: Gets best AI move
  - `get_user_move_with_timer()`: Handles user input with timer
  - `play()`: Main game loop

## Tips for Playing

1. **Think Ahead**: Plan your strategy, you have 15 seconds per move
2. **Develop Pieces**: Move knights and bishops early
3. **Control the Center**: Occupy central squares (e4, e5, d4, d5)
4. **Protect Your King**: Castle early for king safety
5. **Use Timer Wisely**: Don't rush, but don't run out of time
6. **Check Move History**: Use 'history' command to review the game

## Troubleshooting

### Import Error
If you get an import error, make sure python-chess is installed:
```bash
pip install python-chess
```

### Input Timeout Not Working
The timer uses threading. On some systems, input with timeout may not work perfectly. The game will still function, but the timer may be less accurate.

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.

## Author

Created as a demonstration of chess AI implementation using Minimax algorithm with Alpha-Beta pruning.

---

Enjoy the game! / खेल का आनंद लें!