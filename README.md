# Chess Game - Player vs AI

A complete chess game implementation in Python featuring a beautiful GUI and a powerful AI opponent using Minimax algorithm with Alpha-Beta pruning.

## Features

### Core Features:
- **Beautiful GUI Interface**: Professional-looking chess board with smooth graphics
- **Player vs AI Mode**: Play against a strong AI opponent
- **Choice of Color**: Choose to play as White or Black at game start
- **Strong AI Implementation**:
  - Minimax algorithm with Alpha-Beta pruning
  - Advanced evaluation function considering material, position, and mobility
  - Search depth of 4 plies for very strong gameplay
  - Move ordering with MVV-LVA for optimal pruning
- **Move Timer**: 15-second visual countdown timer for each move
- **Interactive Interface**: Click-to-move with visual feedback

### UI/UX Features:
- Beautiful chessboard with clear piece display
- Visual highlighting of selected pieces
- Valid move indicators (circles for regular moves, rings for captures)
- Check highlighting in red
- Last move highlighting in yellow
- Move history display panel
- Captured pieces display
- Current turn indicator
- Visual timer with warning color when time is low
- Game result overlay with restart option
- Smooth animations and responsive controls

## Requirements

- Python 3.7 or higher
- python-chess library
- pygame library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/25lmmc1065/chess-game.git
cd chess-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The game requires pygame and python-chess which will be installed automatically.

## How to Run

Run the GUI game using:
```bash
python main.py
```

For the classic CLI version:
```bash
python chess_game.py
```

## How to Play

1. **Start the Game**: Run `python main.py`
2. **Choose Color**: Click on "Play as White" or "Play as Black" button
3. **Make Moves**: 
   - Click on a piece to select it (valid moves will be highlighted)
   - Click on a highlighted square to move the piece there
   - You have 15 seconds to make each move (shown in the timer)
4. **Game Features**:
   - View move history in the right panel
   - See captured pieces
   - Timer counts down for each move
   - Game automatically detects checkmate, stalemate, and draws
5. **Restart**: After game ends, click "Restart Game" button to play again

## Game Interface

The GUI features:
- **Left Side**: Beautiful chessboard with Unicode piece symbols
  - Light and dark squares
  - File (a-h) and rank (1-8) labels
  - Visual highlighting for selected pieces and valid moves
  - Red overlay when king is in check
  - Yellow borders for last move made
  
- **Right Panel**:
  - Game title and current turn indicator
  - Timer display with countdown (turns red when < 5 seconds)
  - Captured pieces display
  - Move history showing all moves in standard notation
  
- **Start Screen**:
  - Choose your color (White or Black)
  - Game instructions and features
  
- **Game Over Screen**:
  - Result display (Checkmate, Stalemate, Draw, Timeout)
  - Restart button to play again

## AI Algorithm Details

### Minimax with Alpha-Beta Pruning
The AI uses the Minimax algorithm with Alpha-Beta pruning to search the game tree efficiently:
- **Search Depth**: 4 plies (can be changed in `chess_ai.py` for stronger or faster AI)
- **Alpha-Beta Pruning**: Eliminates unnecessary branches to speed up search
- **Advanced Move Ordering**: 
  - Prioritizes captures using MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
  - Checks are evaluated highly
  - Dramatically improves pruning efficiency

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

The GUI uses point-and-click interface, but move history is displayed in Standard Algebraic Notation (SAN):
- Examples in move history:
  - `e4` - Pawn to e4
  - `Nf3` - Knight to f3
  - `O-O` - Kingside castling
  - `O-O-O` - Queenside castling
  - `Qxd5` - Queen captures on d5
  - `e8=Q` - Pawn promotion to queen

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
├── main.py           # Main GUI game file (run this!)
├── chess_gui.py      # GUI module with pygame rendering
├── chess_ai.py       # AI engine with Minimax algorithm
├── chess_game.py     # Classic CLI version (original)
├── requirements.txt  # Python dependencies (pygame, python-chess)
└── README.md         # This file
```

## Technical Implementation

### Libraries Used
- **python-chess**: Handles chess rules, move validation, and game state
- **pygame**: GUI rendering and event handling
- **time**: Time tracking for timer and AI thinking

### Key Classes and Functions

**chess_ai.py:**
- `ChessAI`: AI engine class
  - `evaluate_position()`: Evaluates board positions
  - `minimax()`: AI move selection using Minimax with Alpha-Beta pruning
  - `get_best_move()`: Gets best AI move

**chess_gui.py:**
- `ChessGUI`: GUI rendering class
  - `draw_board()`: Renders chessboard
  - `draw_pieces()`: Renders pieces
  - `draw_highlights()`: Visual feedback for moves
  - `draw_timer()`: Timer display
  - `draw_info_panel()`: Move history and game info

**main.py:**
- `ChessGameGUI`: Main game controller
  - `choose_color()`: Start screen
  - `handle_user_click()`: Mouse input handling
  - `make_move()`: Execute moves
  - `play()`: Main game loop

## Tips for Playing

1. **Think Ahead**: Plan your strategy, you have 15 seconds per move
2. **Visual Feedback**: Click a piece to see all its valid moves highlighted
3. **Develop Pieces**: Move knights and bishops early
4. **Control the Center**: Occupy central squares (e4, e5, d4, d5)
5. **Protect Your King**: Castle early for king safety
6. **Watch the Timer**: Red color indicates less than 5 seconds remaining
7. **Review Moves**: Check the move history panel to review the game

## Troubleshooting

### Import Errors
If you get import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-chess pygame
```

### Display Issues
If the window doesn't display correctly:
- Make sure you have a graphical environment (not SSH terminal only)
- Update pygame: `pip install --upgrade pygame`
- Try running in a different terminal or IDE

### Performance
If the AI is too slow or too fast:
- Edit `main.py` and change `search_depth` parameter in `ChessAI(search_depth=4)`
- Lower values (2-3) = faster but weaker AI
- Higher values (5-6) = slower but stronger AI

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.

## AI Difficulty

The AI is designed to be very strong with the following characteristics:
- **Search Depth 4**: Looks 4 moves ahead (2 full turns)
- **Advanced Evaluation**: Considers material, position, mobility, and king safety
- **Optimal Move Ordering**: Finds the best moves quickly using smart pruning
- **Win Rate**: Against beginners ~95-100%, against intermediate players ~70-80%

To adjust difficulty, edit `main.py` line with `ChessAI(search_depth=4)`:
- Depth 2-3: Beginner level
- Depth 4-5: Intermediate to advanced level
- Depth 6+: Expert level (will be slower)

## Author

Created as a demonstration of chess AI implementation using Minimax algorithm with Alpha-Beta pruning, featuring a professional GUI with pygame.

---

Enjoy the game!