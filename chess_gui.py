#!/usr/bin/env python3
"""
Chess Game GUI Module
Handles all graphical rendering and user interactions
"""

import pygame
import chess
import time
from typing import Optional, Tuple, List

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68, 150)
VALID_MOVE_COLOR = (100, 249, 83, 150)
CHECK_COLOR = (255, 0, 0, 150)
BOARD_BORDER_COLOR = (60, 40, 20)
BG_COLOR = (49, 46, 43)
TEXT_COLOR = (255, 255, 255)
TIMER_WARNING_COLOR = (255, 100, 100)
PANEL_BG_COLOR = (40, 40, 40)

# Board dimensions
SQUARE_SIZE = 70
BOARD_SIZE = SQUARE_SIZE * 8
PANEL_WIDTH = 300
WINDOW_WIDTH = BOARD_SIZE + PANEL_WIDTH + 40
WINDOW_HEIGHT = BOARD_SIZE + 100
BOARD_OFFSET_X = 20
BOARD_OFFSET_Y = 50

# Piece Unicode symbols
PIECE_SYMBOLS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}


class ChessGUI:
    """Chess GUI using Pygame"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game - Player vs AI")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 40)
        self.large_font = pygame.font.Font(None, 60)
        self.piece_font = pygame.font.Font(None, 65)
        self.info_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Game state
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        self.game_over = False
        self.game_result = None
        
    def draw_board(self, board: chess.Board, flip_board: bool = False):
        """Draw the chess board"""
        for rank in range(8):
            for file in range(8):
                # Calculate position
                if flip_board:
                    x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
                else:
                    x = BOARD_OFFSET_X + file * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
                
                # Draw square
                color = WHITE if (rank + file) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw file/rank labels
                if rank == 0:
                    label = chr(ord('a') + file) if not flip_board else chr(ord('h') - file)
                    text = self.small_font.render(label, True, BLACK if color == WHITE else WHITE)
                    self.screen.blit(text, (x + SQUARE_SIZE - 15, y + SQUARE_SIZE - 18))
                
                if file == 0:
                    label = str(rank + 1)
                    text = self.small_font.render(label, True, BLACK if color == WHITE else WHITE)
                    self.screen.blit(text, (x + 5, y + 3))
        
        # Draw border
        pygame.draw.rect(self.screen, BOARD_BORDER_COLOR, 
                        (BOARD_OFFSET_X - 3, BOARD_OFFSET_Y - 3, 
                         BOARD_SIZE + 6, BOARD_SIZE + 6), 3)
    
    def draw_pieces(self, board: chess.Board, flip_board: bool = False):
        """Draw all pieces on the board"""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                
                if flip_board:
                    x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
                else:
                    x = BOARD_OFFSET_X + file * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
                
                # Draw piece symbol
                symbol = PIECE_SYMBOLS[piece.symbol()]
                color = (255, 255, 255) if piece.color == chess.WHITE else (0, 0, 0)
                
                text = self.piece_font.render(symbol, True, color)
                text_rect = text.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                self.screen.blit(text, text_rect)
    
    def draw_highlights(self, board: chess.Board, flip_board: bool = False):
        """Draw highlighted squares for selected piece and valid moves"""
        # Highlight selected square
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = chess.square_rank(self.selected_square)
            
            if flip_board:
                x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
            else:
                x = BOARD_OFFSET_X + file * SQUARE_SIZE
                y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
            
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            surface.fill(HIGHLIGHT_COLOR)
            self.screen.blit(surface, (x, y))
        
        # Highlight valid moves
        for move in self.valid_moves:
            file = chess.square_file(move.to_square)
            rank = chess.square_rank(move.to_square)
            
            if flip_board:
                x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
            else:
                x = BOARD_OFFSET_X + file * SQUARE_SIZE
                y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
            
            # Draw circle for valid move
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            if board.piece_at(move.to_square):  # Capture move
                pygame.draw.circle(surface, VALID_MOVE_COLOR, 
                                 (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                                 SQUARE_SIZE // 2 - 5, 5)
            else:  # Normal move
                pygame.draw.circle(surface, VALID_MOVE_COLOR, 
                                 (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 12)
            self.screen.blit(surface, (x, y))
        
        # Highlight check
        if board.is_check():
            king_square = board.king(board.turn)
            if king_square is not None:
                file = chess.square_file(king_square)
                rank = chess.square_rank(king_square)
                
                if flip_board:
                    x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
                else:
                    x = BOARD_OFFSET_X + file * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
                
                surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                surface.fill(CHECK_COLOR)
                self.screen.blit(surface, (x, y))
        
        # Highlight last move
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                
                if flip_board:
                    x = BOARD_OFFSET_X + (7 - file) * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + rank * SQUARE_SIZE
                else:
                    x = BOARD_OFFSET_X + file * SQUARE_SIZE
                    y = BOARD_OFFSET_Y + (7 - rank) * SQUARE_SIZE
                
                pygame.draw.rect(self.screen, (255, 255, 0), 
                               (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
    
    def draw_timer(self, time_remaining: float, is_user_turn: bool):
        """Draw the move timer"""
        panel_x = BOARD_OFFSET_X + BOARD_SIZE + 20
        timer_y = BOARD_OFFSET_Y + 100
        
        # Timer background
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, 
                        (panel_x, timer_y, PANEL_WIDTH - 20, 80))
        pygame.draw.rect(self.screen, TEXT_COLOR, 
                        (panel_x, timer_y, PANEL_WIDTH - 20, 80), 2)
        
        # Timer text
        player = "Your Turn" if is_user_turn else "AI Thinking"
        text = self.info_font.render(player, True, TEXT_COLOR)
        self.screen.blit(text, (panel_x + 10, timer_y + 10))
        
        # Time display
        time_color = TIMER_WARNING_COLOR if time_remaining < 5 else TEXT_COLOR
        time_text = f"{max(0, int(time_remaining))}s"
        text = self.large_font.render(time_text, True, time_color)
        text_rect = text.get_rect(center=(panel_x + (PANEL_WIDTH - 20) // 2, timer_y + 50))
        self.screen.blit(text, text_rect)
    
    def draw_info_panel(self, board: chess.Board, move_history: List[str], 
                       captured_white: List, captured_black: List):
        """Draw information panel with move history and captured pieces"""
        panel_x = BOARD_OFFSET_X + BOARD_SIZE + 20
        
        # Title
        title = self.title_font.render("Chess Game", True, TEXT_COLOR)
        self.screen.blit(title, (panel_x, 10))
        
        # Current turn
        turn_y = BOARD_OFFSET_Y + 200
        turn_text = "White to move" if board.turn == chess.WHITE else "Black to move"
        text = self.info_font.render(turn_text, True, TEXT_COLOR)
        self.screen.blit(text, (panel_x, turn_y))
        
        # Game status
        status_y = turn_y + 35
        if board.is_check():
            status = self.info_font.render("CHECK!", True, (255, 100, 100))
            self.screen.blit(status, (panel_x, status_y))
        
        # Captured pieces
        captured_y = status_y + 50
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, 
                        (panel_x, captured_y, PANEL_WIDTH - 20, 100))
        
        cap_title = self.small_font.render("Captured:", True, TEXT_COLOR)
        self.screen.blit(cap_title, (panel_x + 5, captured_y + 5))
        
        # White captured
        if captured_white:
            white_pieces = ' '.join([PIECE_SYMBOLS[p.symbol()] for p in captured_white])
            text = self.info_font.render(white_pieces, True, (255, 255, 255))
            self.screen.blit(text, (panel_x + 5, captured_y + 30))
        
        # Black captured
        if captured_black:
            black_pieces = ' '.join([PIECE_SYMBOLS[p.symbol()] for p in captured_black])
            text = self.info_font.render(black_pieces, True, (0, 0, 0))
            self.screen.blit(text, (panel_x + 5, captured_y + 60))
        
        # Move history
        history_y = captured_y + 110
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, 
                        (panel_x, history_y, PANEL_WIDTH - 20, 
                         WINDOW_HEIGHT - history_y - 20))
        
        hist_title = self.small_font.render("Move History:", True, TEXT_COLOR)
        self.screen.blit(hist_title, (panel_x + 5, history_y + 5))
        
        # Display last 10 moves
        y_offset = history_y + 30
        start_idx = max(0, len(move_history) - 20)
        for i in range(start_idx, len(move_history), 2):
            move_num = (i // 2) + 1
            white_move = move_history[i] if i < len(move_history) else ""
            black_move = move_history[i + 1] if i + 1 < len(move_history) else ""
            
            move_text = f"{move_num}. {white_move}"
            if black_move:
                move_text += f" {black_move}"
            
            text = self.small_font.render(move_text, True, TEXT_COLOR)
            self.screen.blit(text, (panel_x + 5, y_offset))
            y_offset += 25
            
            if y_offset > WINDOW_HEIGHT - 40:
                break
    
    def draw_game_over_overlay(self, result_text: str):
        """Draw game over overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Result text
        text = self.large_font.render(result_text, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Restart button
        button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50)
        pygame.draw.rect(self.screen, (100, 150, 100), button_rect)
        pygame.draw.rect(self.screen, TEXT_COLOR, button_rect, 3)
        
        restart_text = self.info_font.render("Restart Game", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=button_rect.center)
        self.screen.blit(restart_text, restart_rect)
        
        return button_rect
    
    def draw_start_screen(self):
        """Draw start screen for choosing color"""
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.large_font.render("Chess Game", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.info_font.render("Player vs AI", True, TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        inst = self.info_font.render("Choose your color:", True, TEXT_COLOR)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(inst, inst_rect)
        
        # White button
        white_button = pygame.Rect(WINDOW_WIDTH // 2 - 250, 320, 200, 80)
        pygame.draw.rect(self.screen, WHITE, white_button)
        pygame.draw.rect(self.screen, BOARD_BORDER_COLOR, white_button, 3)
        
        white_text = self.info_font.render("Play as White", True, (0, 0, 0))
        white_rect = white_text.get_rect(center=white_button.center)
        self.screen.blit(white_text, white_rect)
        
        # Black button
        black_button = pygame.Rect(WINDOW_WIDTH // 2 + 50, 320, 200, 80)
        pygame.draw.rect(self.screen, BLACK, black_button)
        pygame.draw.rect(self.screen, BOARD_BORDER_COLOR, black_button, 3)
        
        black_text = self.info_font.render("Play as Black", True, TEXT_COLOR)
        black_rect = black_text.get_rect(center=black_button.center)
        self.screen.blit(black_text, black_rect)
        
        # Info text
        info_lines = [
            "• 15 seconds per move",
            "• Click piece to see valid moves",
            "• AI uses advanced Minimax algorithm"
        ]
        y = 450
        for line in info_lines:
            text = self.small_font.render(line, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
        
        pygame.display.flip()
        return white_button, black_button
    
    def get_square_from_pos(self, pos: Tuple[int, int], flip_board: bool = False) -> Optional[int]:
        """Convert screen position to chess square"""
        x, y = pos
        
        # Check if click is within board
        if (x < BOARD_OFFSET_X or x >= BOARD_OFFSET_X + BOARD_SIZE or
            y < BOARD_OFFSET_Y or y >= BOARD_OFFSET_Y + BOARD_SIZE):
            return None
        
        # Calculate file and rank
        file = (x - BOARD_OFFSET_X) // SQUARE_SIZE
        rank = 7 - ((y - BOARD_OFFSET_Y) // SQUARE_SIZE)
        
        if flip_board:
            file = 7 - file
            rank = 7 - rank
        
        return chess.square(file, rank)
    
    def render(self, board: chess.Board, time_remaining: float, is_user_turn: bool,
               move_history: List[str], captured_white: List, captured_black: List,
               flip_board: bool = False):
        """Render the complete game state"""
        self.screen.fill(BG_COLOR)
        
        # Draw board and pieces
        self.draw_board(board, flip_board)
        self.draw_highlights(board, flip_board)
        self.draw_pieces(board, flip_board)
        
        # Draw UI elements
        self.draw_timer(time_remaining, is_user_turn)
        self.draw_info_panel(board, move_history, captured_white, captured_black)
        
        # Draw game over overlay if game ended
        if self.game_over and self.game_result:
            return self.draw_game_over_overlay(self.game_result)
        
        pygame.display.flip()
        return None
