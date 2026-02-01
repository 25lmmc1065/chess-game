#!/usr/bin/env python3
"""
Chess Game with AI - Player vs AI
Features: Minimax with Alpha-Beta pruning, Move timer, Hindi language support
"""

import chess
import time
import sys
import threading
from typing import Optional, Tuple, List

# Piece values for evaluation
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-square tables for positional evaluation
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MIDDLE_GAME_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

KING_END_GAME_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

class ChessGame:
    """Main Chess Game class"""
    
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.user_is_white = True
        self.move_time_limit = 15  # seconds
        self.search_depth = 3  # AI search depth
        self.timeout_occurred = False
        
    def display_board(self):
        """Display the chess board in ASCII format"""
        print("\n  a b c d e f g h")
        board_str = str(self.board)
        lines = board_str.split('\n')
        for i, line in enumerate(lines):
            rank = 8 - i
            print(f"{rank} {line}")
        print()
        
    def get_piece_unicode(self, piece):
        """Get Unicode representation of chess piece"""
        symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        return symbols.get(piece.symbol(), piece.symbol())
    
    def display_captured_pieces(self):
        """Display captured pieces"""
        if self.captured_white or self.captured_black:
            print("Captured Pieces / पकड़े गए मोहरे:")
            if self.captured_white:
                print(f"  White / सफेद: {' '.join([self.get_piece_unicode(p) for p in self.captured_white])}")
            if self.captured_black:
                print(f"  Black / काला: {' '.join([self.get_piece_unicode(p) for p in self.captured_black])}")
            print()
    
    def display_game_status(self):
        """Display current game status"""
        if self.board.is_checkmate():
            winner = "Black / काला" if self.board.turn == chess.WHITE else "White / सफेद"
            print(f"\n{'='*50}")
            print(f"Checkmate! {winner} wins! / शह और मात! {winner} जीत गया!")
            print(f"{'='*50}\n")
            return True
        elif self.board.is_stalemate():
            print(f"\n{'='*50}")
            print("Stalemate! Game is a draw! / गतिरोध! खेल ड्रॉ है!")
            print(f"{'='*50}\n")
            return True
        elif self.board.is_insufficient_material():
            print(f"\n{'='*50}")
            print("Draw by insufficient material! / अपर्याप्त सामग्री से ड्रॉ!")
            print(f"{'='*50}\n")
            return True
        elif self.board.is_seventyfive_moves():
            print(f"\n{'='*50}")
            print("Draw by 75-move rule! / 75-चाल नियम से ड्रॉ!")
            print(f"{'='*50}\n")
            return True
        elif self.board.is_fivefold_repetition():
            print(f"\n{'='*50}")
            print("Draw by fivefold repetition! / पांच बार दोहराव से ड्रॉ!")
            print(f"{'='*50}\n")
            return True
        elif self.board.is_check():
            print("Check! / शह!")
        
        return False
    
    def evaluate_position(self, board: chess.Board) -> int:
        """
        Evaluate the current board position
        Returns a score from white's perspective (positive = white advantage)
        """
        if board.is_checkmate():
            return -20000 if board.turn == chess.WHITE else 20000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        # Count material for both sides
        white_material = 0
        black_material = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            value = PIECE_VALUES[piece.piece_type]
            pos_value = self.get_position_value(piece, square)
            
            if piece.color == chess.WHITE:
                white_material += value + pos_value
            else:
                black_material += value + pos_value
        
        score = white_material - black_material
        
        # Mobility bonus (number of legal moves)
        mobility = len(list(board.legal_moves))
        if board.turn == chess.WHITE:
            score += mobility * 5
        else:
            score -= mobility * 5
        
        return score
    
    def get_position_value(self, piece, square):
        """Get positional value for a piece on a square"""
        piece_type = piece.piece_type
        
        # Flip square for black pieces
        if piece.color == chess.BLACK:
            square = chess.square_mirror(square)
        
        if piece_type == chess.PAWN:
            return PAWN_TABLE[square]
        elif piece_type == chess.KNIGHT:
            return KNIGHT_TABLE[square]
        elif piece_type == chess.BISHOP:
            return BISHOP_TABLE[square]
        elif piece_type == chess.ROOK:
            return ROOK_TABLE[square]
        elif piece_type == chess.QUEEN:
            return QUEEN_TABLE[square]
        elif piece_type == chess.KING:
            # Use endgame table if few pieces remain
            if len(self.board.piece_map()) <= 10:
                return KING_END_GAME_TABLE[square]
            else:
                return KING_MIDDLE_GAME_TABLE[square]
        
        return 0
    
    def minimax(self, board: chess.Board, depth: int, alpha: int, beta: int, 
                maximizing: bool) -> Tuple[int, Optional[chess.Move]]:
        """
        Minimax algorithm with Alpha-Beta pruning
        Returns (evaluation, best_move)
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None
        
        best_move = None
        legal_moves = list(board.legal_moves)
        
        # Move ordering: prioritize captures
        legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)
        
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move
    
    def get_ai_move(self) -> Optional[chess.Move]:
        """Get the best move for AI using Minimax with Alpha-Beta pruning"""
        print("AI is thinking... / AI सोच रहा है...")
        start_time = time.time()
        
        # AI plays as white or black
        maximizing = (self.board.turn == chess.WHITE and not self.user_is_white) or \
                     (self.board.turn == chess.BLACK and self.user_is_white)
        
        _, best_move = self.minimax(
            self.board, 
            self.search_depth, 
            float('-inf'), 
            float('inf'), 
            maximizing
        )
        
        elapsed = time.time() - start_time
        print(f"AI thought for {elapsed:.2f} seconds / AI ने {elapsed:.2f} सेकंड सोचा")
        
        return best_move
    
    def get_user_move_with_timer(self) -> Optional[chess.Move]:
        """Get user move with a timer"""
        move_input = [None]
        self.timeout_occurred = False
        
        def get_input():
            try:
                move_input[0] = input("Enter move (e.g., e2e4) / चाल दर्ज करें: ").strip()
            except EOFError:
                move_input[0] = None
        
        print(f"Time remaining: {self.move_time_limit} seconds / शेष समय: {self.move_time_limit} सेकंड")
        
        # Start input thread
        input_thread = threading.Thread(target=get_input)
        input_thread.daemon = True
        input_thread.start()
        
        # Wait for input with timer
        start_time = time.time()
        while input_thread.is_alive():
            elapsed = time.time() - start_time
            if elapsed >= self.move_time_limit:
                self.timeout_occurred = True
                print(f"\n\nTime's up! / समय समाप्त!")
                return None
            
            remaining = self.move_time_limit - int(elapsed)
            if remaining > 0 and int(elapsed) < self.move_time_limit:
                time.sleep(0.1)
        
        # Parse the move
        if move_input[0] is None:
            return None
        
        # Handle special commands
        if move_input[0].lower() in ['resign', 'quit', 'exit']:
            return 'resign'
        
        if move_input[0].lower() == 'history':
            self.display_move_history()
            return self.get_user_move_with_timer()
        
        # Try to parse the move
        try:
            move = chess.Move.from_uci(move_input[0])
            if move in self.board.legal_moves:
                return move
            else:
                print("Illegal move! / अवैध चाल!")
                return self.get_user_move_with_timer()
        except:
            # Try SAN notation
            try:
                move = self.board.parse_san(move_input[0])
                return move
            except:
                print("Invalid move format! Please use format like 'e2e4' or 'Nf3' / अवैध चाल प्रारूप!")
                return self.get_user_move_with_timer()
    
    def display_move_history(self):
        """Display move history"""
        if not self.move_history:
            print("\nNo moves yet! / अभी तक कोई चाल नहीं!\n")
            return
        
        print("\n" + "="*50)
        print("Move History / चाल इतिहास:")
        print("="*50)
        for i, move in enumerate(self.move_history, 1):
            if i % 2 == 1:
                print(f"{(i+1)//2}. {move}", end=" ")
            else:
                print(move)
        if len(self.move_history) % 2 == 1:
            print()
        print("="*50 + "\n")
    
    def make_move(self, move: chess.Move):
        """Make a move on the board"""
        # Check if it's a capture
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            if captured_piece.color == chess.WHITE:
                self.captured_white.append(captured_piece)
            else:
                self.captured_black.append(captured_piece)
        
        # Make the move
        san_move = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san_move)
        
        print(f"\nMove played: {san_move}")
        print(f"चाल खेली गई: {san_move}\n")
    
    def choose_first_player(self):
        """Let user choose who plays first"""
        print("="*50)
        print("Welcome to Chess Game! / शतरंज के खेल में आपका स्वागत है!")
        print("="*50)
        print("\nChoose who plays first / चुनें कौन पहले खेलेगा:")
        print("1. User (White) / उपयोगकर्ता (सफेद)")
        print("2. AI (White) / AI (सफेद)")
        
        while True:
            try:
                choice = input("\nEnter choice (1/2) / विकल्प दर्ज करें (1/2): ").strip()
                if choice == '1':
                    self.user_is_white = True
                    print("\nYou are playing as White! / आप सफेद के रूप में खेल रहे हैं!")
                    break
                elif choice == '2':
                    self.user_is_white = False
                    print("\nYou are playing as Black! / आप काले के रूप में खेल रहे हैं!")
                    break
                else:
                    print("Invalid choice! Please enter 1 or 2 / अवैध विकल्प! कृपया 1 या 2 दर्ज करें")
            except EOFError:
                print("\nDefaulting to User as White / डिफ़ॉल्ट रूप से उपयोगकर्ता सफेद है")
                self.user_is_white = True
                break
    
    def play(self):
        """Main game loop"""
        self.choose_first_player()
        
        print("\n" + "="*50)
        print("Game Instructions / खेल निर्देश:")
        print("="*50)
        print("- Enter moves in UCI format (e.g., e2e4) or SAN format (e.g., Nf3)")
        print("  UCI प्रारूप में चाल दर्ज करें (जैसे, e2e4) या SAN प्रारूप (जैसे, Nf3)")
        print("- Type 'history' to see move history / चाल इतिहास देखने के लिए 'history' टाइप करें")
        print("- Type 'resign' to resign / हार मानने के लिए 'resign' टाइप करें")
        print("- You have 15 seconds per move / आपके पास प्रति चाल 15 सेकंड हैं")
        print("="*50 + "\n")
        
        turn_number = 1
        
        while not self.board.is_game_over():
            self.display_board()
            self.display_captured_pieces()
            
            # Determine whose turn it is
            is_user_turn = (self.board.turn == chess.WHITE and self.user_is_white) or \
                          (self.board.turn == chess.BLACK and not self.user_is_white)
            
            current_player = "White" if self.board.turn == chess.WHITE else "Black"
            current_player_hindi = "सफेद" if self.board.turn == chess.WHITE else "काला"
            
            print(f"Turn {turn_number} - {current_player} to move / चाल {turn_number} - {current_player_hindi} की बारी")
            
            if self.display_game_status():
                break
            
            if is_user_turn:
                print(f"\nYour turn ({current_player}) / आपकी बारी ({current_player_hindi})")
                move = self.get_user_move_with_timer()
                
                if move == 'resign':
                    print(f"\n{current_player} resigned! / {current_player_hindi} ने हार मान ली!")
                    winner = "Black / काला" if current_player == "White" else "White / सफेद"
                    print(f"{winner} wins! / {winner} जीत गया!")
                    break
                
                if move is None:
                    if self.timeout_occurred:
                        print(f"{current_player} ran out of time! / {current_player_hindi} का समय समाप्त हो गया!")
                        winner = "Black / काला" if current_player == "White" else "White / सफेद"
                        print(f"{winner} wins! / {winner} जीत गया!")
                        break
                    else:
                        continue
            else:
                print(f"\nAI's turn ({current_player}) / AI की बारी ({current_player_hindi})")
                move = self.get_ai_move()
                
                if move is None:
                    print("AI couldn't find a move! / AI को कोई चाल नहीं मिली!")
                    break
            
            self.make_move(move)
            
            if self.board.turn == chess.WHITE:
                turn_number += 1
        
        # Final board display
        self.display_board()
        self.display_captured_pieces()
        self.display_game_status()
        self.display_move_history()
        
        print("\n" + "="*50)
        print("Thank you for playing! / खेलने के लिए धन्यवाद!")
        print("="*50 + "\n")


def main():
    """Main function to start the game"""
    game = ChessGame()
    game.play()


if __name__ == "__main__":
    main()
