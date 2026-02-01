#!/usr/bin/env python3
"""
Chess Game - Player vs AI with GUI
Main game file that integrates GUI and AI engine
"""

import pygame
import chess
import time
import sys
from typing import Optional
from chess_gui import ChessGUI
from chess_ai import ChessAI


class ChessGameGUI:
    """Main Chess Game with GUI"""
    
    def __init__(self):
        self.board = chess.Board()
        self.gui = ChessGUI()
        self.ai = ChessAI(search_depth=4)  # Depth 4 for strong AI
        
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.user_is_white = True
        self.move_time_limit = 15  # seconds
        
        self.move_start_time = None
        self.game_over = False
        self.running = True
        
    def choose_color(self) -> bool:
        """Let user choose color at start screen"""
        white_button, black_button = self.gui.draw_start_screen()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if white_button.collidepoint(pos):
                        self.user_is_white = True
                        return True
                    elif black_button.collidepoint(pos):
                        self.user_is_white = False
                        return True
        
        return False
    
    def handle_user_click(self, pos) -> Optional[chess.Move]:
        """Handle user click on the board"""
        flip_board = not self.user_is_white
        square = self.gui.get_square_from_pos(pos, flip_board)
        
        if square is None:
            return None
        
        # If no piece is selected, select the clicked piece
        if self.gui.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.gui.selected_square = square
                # Get valid moves for this piece
                self.gui.valid_moves = [
                    move for move in self.board.legal_moves 
                    if move.from_square == square
                ]
        else:
            # Check if clicked square is a valid move
            move = None
            for valid_move in self.gui.valid_moves:
                if valid_move.to_square == square:
                    move = valid_move
                    break
            
            if move:
                # Check for pawn promotion
                if self.board.piece_at(move.from_square).piece_type == chess.PAWN:
                    if chess.square_rank(move.to_square) in [0, 7]:
                        # Auto-promote to queen
                        move = chess.Move(move.from_square, move.to_square, chess.QUEEN)
                
                self.gui.selected_square = None
                self.gui.valid_moves = []
                return move
            else:
                # Deselect or select new piece
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.gui.selected_square = square
                    self.gui.valid_moves = [
                        move for move in self.board.legal_moves 
                        if move.from_square == square
                    ]
                else:
                    self.gui.selected_square = None
                    self.gui.valid_moves = []
        
        return None
    
    def make_move(self, move: chess.Move, animate: bool = True):
        """Make a move on the board"""
        # Start animation if enabled
        flip_board = not self.user_is_white
        if animate:
            self.gui.start_animation(move, self.board, flip_board)
        
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
        self.gui.last_move = move
    
    def check_game_over(self) -> Optional[str]:
        """Check if game is over and return result text"""
        if self.board.is_checkmate():
            winner = "Black Wins!" if self.board.turn == chess.WHITE else "White Wins!"
            return f"Checkmate! {winner}"
        elif self.board.is_stalemate():
            return "Stalemate! Draw!"
        elif self.board.is_insufficient_material():
            return "Draw! Insufficient Material"
        elif self.board.is_seventyfive_moves():
            return "Draw! 75-Move Rule"
        elif self.board.is_fivefold_repetition():
            return "Draw! Repetition"
        
        return None
    
    def get_ai_move(self) -> Optional[chess.Move]:
        """Get AI move"""
        ai_is_white = not self.user_is_white
        return self.ai.get_best_move(self.board, ai_is_white)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = chess.Board()
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.gui.selected_square = None
        self.gui.valid_moves = []
        self.gui.last_move = None
        self.gui.game_over = False
        self.gui.game_result = None
        self.game_over = False
        self.move_start_time = None
    
    def play(self):
        """Main game loop"""
        # Choose color
        if not self.choose_color():
            return
        
        clock = pygame.time.Clock()
        self.move_start_time = time.time()
        ai_thinking = False
        ai_move = None
        ai_start_time = None
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    # Don't allow clicks during animation
                    if self.gui.is_animating():
                        continue
                    
                    # Determine whose turn it is
                    is_user_turn = (self.board.turn == chess.WHITE and self.user_is_white) or \
                                  (self.board.turn == chess.BLACK and not self.user_is_white)
                    
                    if is_user_turn and not ai_thinking:
                        move = self.handle_user_click(event.pos)
                        if move:
                            self.make_move(move, animate=True)
                            # Animation will complete in the render loop
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    # Check if restart button clicked
                    restart_rect = pygame.Rect(
                        self.gui.screen.get_width() // 2 - 100,
                        self.gui.screen.get_height() // 2 + 20,
                        200, 50
                    )
                    if restart_rect.collidepoint(event.pos):
                        self.reset_game()
                        if not self.choose_color():
                            self.running = False
                        else:
                            self.move_start_time = time.time()
            
            # Check if animation is complete and handle post-move logic
            if self.gui.is_animating():
                # Animation still in progress, skip other logic
                pass
            elif self.gui.animation_start_time is not None:
                # Animation just completed
                self.gui.clear_animation()
                self.move_start_time = time.time()
                
                # Check for game over after animation
                result = self.check_game_over()
                if result:
                    self.game_over = True
                    self.gui.game_over = True
                    self.gui.game_result = result
            
            # Calculate time remaining
            if not self.game_over:
                time_elapsed = time.time() - self.move_start_time
                time_remaining = self.move_time_limit - time_elapsed
                
                # Determine whose turn it is
                is_user_turn = (self.board.turn == chess.WHITE and self.user_is_white) or \
                              (self.board.turn == chess.BLACK and not self.user_is_white)
                
                # Check for timeout (only if not animating)
                if time_remaining <= 0 and not ai_thinking and not self.gui.is_animating():
                    if is_user_turn:
                        result = "Time's Up! " + ("Black Wins!" if self.user_is_white else "White Wins!")
                    else:
                        result = "AI Timeout! " + ("White Wins!" if self.user_is_white else "Black Wins!")
                    
                    self.game_over = True
                    self.gui.game_over = True
                    self.gui.game_result = result
                
                # AI turn (only if no animation in progress)
                if not is_user_turn and not self.game_over and not ai_thinking and not self.gui.is_animating():
                    ai_thinking = True
                    ai_start_time = time.time()
                
                # Process AI move (simulate thinking with minimum delay)
                if ai_thinking and not self.gui.is_animating():
                    ai_thinking_time = time.time() - ai_start_time
                    
                    # Get AI move if not already computed
                    if ai_move is None:
                        ai_move = self.get_ai_move()
                    
                    # Make AI move after small delay for visual feedback (min 0.5s)
                    if ai_thinking_time >= 0.5 and ai_move:
                        self.make_move(ai_move, animate=True)
                        ai_move = None
                        ai_thinking = False
                    
                    # Check AI timeout
                    if time_remaining <= 0:
                        result = "AI Timeout! " + ("White Wins!" if self.user_is_white else "Black Wins!")
                        self.game_over = True
                        self.gui.game_over = True
                        self.gui.game_result = result
                        ai_thinking = False
                        ai_move = None
            else:
                time_remaining = 0
                is_user_turn = False
            
            # Render
            flip_board = not self.user_is_white
            self.gui.render(
                self.board,
                max(0, time_remaining),
                is_user_turn and not ai_thinking,
                self.move_history,
                self.captured_white,
                self.captured_black,
                flip_board
            )
            
            clock.tick(30)  # 30 FPS
        
        pygame.quit()


def main():
    """Main function to start the game"""
    game = ChessGameGUI()
    game.play()


if __name__ == "__main__":
    main()
