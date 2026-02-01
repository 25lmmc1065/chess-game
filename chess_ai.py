#!/usr/bin/env python3
"""
Chess AI Engine Module
Implements Minimax algorithm with Alpha-Beta pruning and position evaluation
"""

import chess
from typing import Tuple, Optional

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


class ChessAI:
    """Chess AI using Minimax with Alpha-Beta pruning"""
    
    def __init__(self, search_depth: int = 4):
        """
        Initialize Chess AI
        
        Args:
            search_depth: How many moves ahead to search (default: 4)
        """
        self.search_depth = search_depth
        self.nodes_searched = 0
    
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
            pos_value = self.get_position_value(piece, square, board)
            
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
    
    def get_position_value(self, piece, square, board):
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
            if len(board.piece_map()) <= 10:
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
        self.nodes_searched += 1
        
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None
        
        best_move = None
        legal_moves = list(board.legal_moves)
        
        # Move ordering: prioritize captures and checks for better pruning
        def move_priority(move):
            score = 0
            if board.is_capture(move):
                score += 1000
                # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                captured = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                if captured and attacker:
                    score += PIECE_VALUES[captured.piece_type] - PIECE_VALUES[attacker.piece_type] // 10
            
            board.push(move)
            if board.is_check():
                score += 500
            board.pop()
            
            return score
        
        legal_moves.sort(key=move_priority, reverse=True)
        
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
    
    def get_best_move(self, board: chess.Board, ai_is_white: bool) -> Optional[chess.Move]:
        """
        Get the best move for AI
        
        Args:
            board: Current chess board
            ai_is_white: True if AI plays as white
            
        Returns:
            Best move found, or None if no valid move
        """
        self.nodes_searched = 0
        
        # AI maximizes when playing as white (evaluation is from white's perspective)
        maximizing = ai_is_white
        
        _, best_move = self.minimax(
            board, 
            self.search_depth, 
            float('-inf'), 
            float('inf'), 
            maximizing
        )
        
        return best_move
