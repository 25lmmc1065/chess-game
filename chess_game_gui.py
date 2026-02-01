#!/usr/bin/env python3
"""
Chess Game with GUI - Player vs AI
Features: Pygame GUI with clear piece graphics, Minimax with Alpha-Beta pruning, Hindi language support
"""

import chess
import pygame
import time
import sys
import math
from typing import Optional, Tuple, List

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)
SELECTED_COLOR = (246, 246, 105)
LAST_MOVE_COLOR = (205, 210, 106)
CHECK_COLOR = (255, 100, 100)
LEGAL_MOVE_COLOR = (100, 200, 100)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
TEXT_COLOR = (50, 50, 50)
WHITE_PIECE_COLOR = (255, 255, 255)
WHITE_PIECE_OUTLINE = (50, 50, 50)
BLACK_PIECE_COLOR = (30, 30, 30)
BLACK_PIECE_OUTLINE = (200, 200, 200)

# Screen dimensions
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
INFO_PANEL_WIDTH = 280
WINDOW_WIDTH = BOARD_SIZE + INFO_PANEL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE

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


class PieceRenderer:
    """Class to render chess pieces as distinct graphical shapes"""
    
    def __init__(self, square_size):
        self.square_size = square_size
        self.piece_size = int(square_size * 0.85)
        self.piece_cache = {}
        self._create_all_pieces()
    
    def _create_all_pieces(self):
        """Pre-render all chess pieces"""
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            self.piece_cache[piece] = self._create_piece_surface(piece)
    
    def _create_piece_surface(self, piece_char):
        """Create a surface with the chess piece drawn"""
        surface = pygame.Surface((self.piece_size, self.piece_size), pygame.SRCALPHA)
        is_white = piece_char.isupper()
        piece_type = piece_char.upper()
        
        fill_color = WHITE_PIECE_COLOR if is_white else BLACK_PIECE_COLOR
        outline_color = WHITE_PIECE_OUTLINE if is_white else BLACK_PIECE_OUTLINE
        
        center_x = self.piece_size // 2
        center_y = self.piece_size // 2
        
        if piece_type == 'P':
            self._draw_pawn(surface, center_x, center_y, fill_color, outline_color)
        elif piece_type == 'R':
            self._draw_rook(surface, center_x, center_y, fill_color, outline_color)
        elif piece_type == 'N':
            self._draw_knight(surface, center_x, center_y, fill_color, outline_color)
        elif piece_type == 'B':
            self._draw_bishop(surface, center_x, center_y, fill_color, outline_color)
        elif piece_type == 'Q':
            self._draw_queen(surface, center_x, center_y, fill_color, outline_color)
        elif piece_type == 'K':
            self._draw_king(surface, center_x, center_y, fill_color, outline_color)
        
        return surface
    
    def _draw_pawn(self, surface, cx, cy, fill_color, outline_color):
        """Draw a pawn - simple rounded shape with small ball on top"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//4, cy + size//5, size//2, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Body (trapezoid-like)
        body_points = [
            (cx - size//5, cy + size//5),
            (cx + size//5, cy + size//5),
            (cx + size//8, cy - size//10),
            (cx - size//8, cy - size//10)
        ]
        pygame.draw.polygon(surface, fill_color, body_points)
        pygame.draw.polygon(surface, outline_color, body_points, 2)
        
        # Head (circle)
        pygame.draw.circle(surface, fill_color, (cx, cy - size//5), size//5)
        pygame.draw.circle(surface, outline_color, (cx, cy - size//5), size//5, 2)
    
    def _draw_rook(self, surface, cx, cy, fill_color, outline_color):
        """Draw a rook - castle shape with battlements"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//3, cy + size//4, size*2//3, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Body
        body_rect = pygame.Rect(cx - size//4, cy - size//6, size//2, size*2//5)
        pygame.draw.rect(surface, fill_color, body_rect)
        pygame.draw.rect(surface, outline_color, body_rect, 2)
        
        # Top (with battlements)
        top_rect = pygame.Rect(cx - size//3, cy - size//4, size*2//3, size//8)
        pygame.draw.rect(surface, fill_color, top_rect)
        pygame.draw.rect(surface, outline_color, top_rect, 2)
        
        # Battlements (3 on top)
        battlement_width = size//8
        battlement_height = size//8
        for i in range(3):
            bx = cx - size//4 + i * (size//4)
            pygame.draw.rect(surface, fill_color, (bx, cy - size//3 - battlement_height//2, battlement_width, battlement_height))
            pygame.draw.rect(surface, outline_color, (bx, cy - size//3 - battlement_height//2, battlement_width, battlement_height), 2)
    
    def _draw_knight(self, surface, cx, cy, fill_color, outline_color):
        """Draw a knight - horse head shape"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//3, cy + size//4, size*2//3, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Horse head shape (simplified polygon)
        head_points = [
            (cx - size//5, cy + size//4),      # Bottom left
            (cx + size//4, cy + size//4),      # Bottom right
            (cx + size//4, cy),                 # Right side
            (cx + size//6, cy - size//6),      # Upper right
            (cx - size//10, cy - size//3),     # Top (ear area)
            (cx - size//4, cy - size//4),      # Left ear
            (cx - size//3, cy - size//6),      # Forehead
            (cx - size//3, cy + size//10),     # Nose
            (cx - size//5, cy + size//8),      # Chin
        ]
        pygame.draw.polygon(surface, fill_color, head_points)
        pygame.draw.polygon(surface, outline_color, head_points, 2)
        
        # Eye
        eye_x = cx
        eye_y = cy - size//8
        pygame.draw.circle(surface, outline_color, (eye_x, eye_y), size//15)
        
        # Ear detail
        pygame.draw.line(surface, outline_color, (cx - size//6, cy - size//4), (cx - size//10, cy - size//6), 2)
    
    def _draw_bishop(self, surface, cx, cy, fill_color, outline_color):
        """Draw a bishop - tall piece with miter (hat)"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//4, cy + size//4, size//2, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Body (tapered)
        body_points = [
            (cx - size//5, cy + size//4),
            (cx + size//5, cy + size//4),
            (cx + size//10, cy - size//10),
            (cx - size//10, cy - size//10)
        ]
        pygame.draw.polygon(surface, fill_color, body_points)
        pygame.draw.polygon(surface, outline_color, body_points, 2)
        
        # Head (oval)
        head_rect = pygame.Rect(cx - size//7, cy - size//4, size*2//7, size//4)
        pygame.draw.ellipse(surface, fill_color, head_rect)
        pygame.draw.ellipse(surface, outline_color, head_rect, 2)
        
        # Miter top (pointed)
        miter_points = [
            (cx - size//10, cy - size//4),
            (cx + size//10, cy - size//4),
            (cx, cy - size//2 + size//10)
        ]
        pygame.draw.polygon(surface, fill_color, miter_points)
        pygame.draw.polygon(surface, outline_color, miter_points, 2)
        
        # Diagonal slit on miter
        pygame.draw.line(surface, outline_color, (cx - size//15, cy - size//5), (cx + size//15, cy - size//4), 2)
    
    def _draw_queen(self, surface, cx, cy, fill_color, outline_color):
        """Draw a queen - tall with crown and ball decorations"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//3, cy + size//4, size*2//3, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Body (tapered)
        body_points = [
            (cx - size//4, cy + size//4),
            (cx + size//4, cy + size//4),
            (cx + size//8, cy - size//8),
            (cx - size//8, cy - size//8)
        ]
        pygame.draw.polygon(surface, fill_color, body_points)
        pygame.draw.polygon(surface, outline_color, body_points, 2)
        
        # Crown base
        crown_base = pygame.Rect(cx - size//5, cy - size//5, size*2//5, size//8)
        pygame.draw.rect(surface, fill_color, crown_base)
        pygame.draw.rect(surface, outline_color, crown_base, 2)
        
        # Crown points (5 decorative points with balls on top)
        num_crown_points = 5
        for i in range(num_crown_points):
            angle = math.pi + (i / (num_crown_points - 1)) * math.pi
            px = cx + int(size//4 * math.cos(angle))
            py = cy - size//4 + int(size//6 * math.sin(angle))
            
            # Line from crown base to point
            crown_base_x = cx + int((size//5) * math.cos(angle))
            crown_base_y = cy - size//5
            pygame.draw.line(surface, fill_color, (crown_base_x, crown_base_y), (px, py - size//12), 4)
            pygame.draw.line(surface, outline_color, (crown_base_x, crown_base_y), (px, py - size//12), 2)
            
            # Ball on top
            pygame.draw.circle(surface, fill_color, (px, py - size//10), size//12)
            pygame.draw.circle(surface, outline_color, (px, py - size//10), size//12, 2)
    
    def _draw_king(self, surface, cx, cy, fill_color, outline_color):
        """Draw a king - tall with cross on top"""
        size = self.piece_size
        
        # Base
        base_rect = pygame.Rect(cx - size//3, cy + size//4, size*2//3, size//6)
        pygame.draw.rect(surface, fill_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, outline_color, base_rect, 2, border_radius=3)
        
        # Body (tapered)
        body_points = [
            (cx - size//4, cy + size//4),
            (cx + size//4, cy + size//4),
            (cx + size//8, cy - size//10),
            (cx - size//8, cy - size//10)
        ]
        pygame.draw.polygon(surface, fill_color, body_points)
        pygame.draw.polygon(surface, outline_color, body_points, 2)
        
        # Crown/head
        head_rect = pygame.Rect(cx - size//6, cy - size//5, size//3, size//5)
        pygame.draw.ellipse(surface, fill_color, head_rect)
        pygame.draw.ellipse(surface, outline_color, head_rect, 2)
        
        # Cross on top
        cross_thickness = size//10
        # Vertical part
        pygame.draw.rect(surface, fill_color, (cx - cross_thickness//2, cy - size//2 + size//10, cross_thickness, size//4))
        pygame.draw.rect(surface, outline_color, (cx - cross_thickness//2, cy - size//2 + size//10, cross_thickness, size//4), 2)
        # Horizontal part
        pygame.draw.rect(surface, fill_color, (cx - size//8, cy - size//3 - cross_thickness//2, size//4, cross_thickness))
        pygame.draw.rect(surface, outline_color, (cx - size//8, cy - size//3 - cross_thickness//2, size//4, cross_thickness), 2)
    
    def get_piece_surface(self, piece_char):
        """Get the cached piece surface"""
        return self.piece_cache.get(piece_char)


class ChessGameGUI:
    """Main Chess Game GUI class"""
    
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.user_is_white = True
        self.search_depth = 3
        self.selected_square = None
        self.legal_moves_for_selected = []
        self.last_move = None
        self.game_started = False
        self.game_over = False
        self.game_result = ""
        self.ai_thinking = False
        self.status_message = ""
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game / शतरंज खेल")
        
        # Load fonts
        self.font_large = pygame.font.SysFont('arial', 48)
        self.font_medium = pygame.font.SysFont('arial', 24)
        self.font_small = pygame.font.SysFont('arial', 18)
        self.font_tiny = pygame.font.SysFont('arial', 14)
        
        # Piece renderer
        self.piece_renderer = PieceRenderer(SQUARE_SIZE)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                # Calculate square position
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                
                # Determine square color
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE if is_light else DARK_SQUARE
                
                # Draw base square
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Get chess square (considering board orientation)
                if self.user_is_white:
                    chess_square = chess.square(col, 7 - row)
                else:
                    chess_square = chess.square(7 - col, row)
                
                # Highlight last move
                if self.last_move:
                    if chess_square in [self.last_move.from_square, self.last_move.to_square]:
                        pygame.draw.rect(self.screen, LAST_MOVE_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if self.selected_square == chess_square:
                    pygame.draw.rect(self.screen, SELECTED_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight legal moves
                for move in self.legal_moves_for_selected:
                    if move.to_square == chess_square:
                        # Draw circle for legal move indicator
                        center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)
                        if self.board.piece_at(chess_square):
                            # Ring for captures
                            pygame.draw.circle(self.screen, LEGAL_MOVE_COLOR, center, SQUARE_SIZE // 2 - 5, 4)
                        else:
                            # Filled circle for empty squares
                            pygame.draw.circle(self.screen, LEGAL_MOVE_COLOR, center, 12)
                
                # Highlight king in check
                if self.board.is_check():
                    king_square = self.board.king(self.board.turn)
                    if chess_square == king_square:
                        pygame.draw.rect(self.screen, CHECK_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        
        # Draw rank and file labels
        for i in range(8):
            # File labels (a-h)
            if self.user_is_white:
                file_label = chr(ord('a') + i)
            else:
                file_label = chr(ord('h') - i)
            text = self.font_tiny.render(file_label, True, DARK_SQUARE if i % 2 == 0 else LIGHT_SQUARE)
            self.screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 12, BOARD_SIZE - 15))
            
            # Rank labels (1-8)
            if self.user_is_white:
                rank_label = str(8 - i)
            else:
                rank_label = str(i + 1)
            text = self.font_tiny.render(rank_label, True, LIGHT_SQUARE if i % 2 == 0 else DARK_SQUARE)
            self.screen.blit(text, (3, i * SQUARE_SIZE + 3))
    
    def draw_pieces(self):
        """Draw chess pieces on the board"""
        for row in range(8):
            for col in range(8):
                # Get chess square
                if self.user_is_white:
                    chess_square = chess.square(col, 7 - row)
                else:
                    chess_square = chess.square(7 - col, row)
                
                piece = self.board.piece_at(chess_square)
                if piece:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE
                    
                    # Get piece surface
                    piece_char = piece.symbol()
                    piece_surface = self.piece_renderer.get_piece_surface(piece_char)
                    
                    if piece_surface:
                        # Center piece in square
                        piece_x = x + (SQUARE_SIZE - piece_surface.get_width()) // 2
                        piece_y = y + (SQUARE_SIZE - piece_surface.get_height()) // 2
                        self.screen.blit(piece_surface, (piece_x, piece_y))
    
    def draw_info_panel(self):
        """Draw the information panel on the right side"""
        # Panel background
        panel_rect = pygame.Rect(BOARD_SIZE, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.line(self.screen, (200, 200, 200), (BOARD_SIZE, 0), (BOARD_SIZE, WINDOW_HEIGHT), 2)
        
        y_offset = 15
        
        # Title
        title = self.font_medium.render("Chess / शतरंज", True, TEXT_COLOR)
        self.screen.blit(title, (BOARD_SIZE + 15, y_offset))
        y_offset += 40
        
        # Game status
        if self.game_over:
            status = self.font_medium.render(self.game_result, True, (200, 0, 0))
            self.screen.blit(status, (BOARD_SIZE + 15, y_offset))
            y_offset += 30
        elif self.ai_thinking:
            status = self.font_small.render("AI thinking... / AI सोच रहा है...", True, (0, 100, 0))
            self.screen.blit(status, (BOARD_SIZE + 15, y_offset))
            y_offset += 25
        else:
            turn_text = "White / सफेद" if self.board.turn == chess.WHITE else "Black / काला"
            is_your_turn = (self.board.turn == chess.WHITE and self.user_is_white) or \
                          (self.board.turn == chess.BLACK and not self.user_is_white)
            
            if is_your_turn:
                status = self.font_small.render(f"Your turn ({turn_text})", True, (0, 100, 0))
            else:
                status = self.font_small.render(f"AI's turn ({turn_text})", True, (100, 100, 100))
            self.screen.blit(status, (BOARD_SIZE + 15, y_offset))
            y_offset += 25
        
        if self.status_message:
            msg = self.font_small.render(self.status_message, True, (200, 100, 0))
            self.screen.blit(msg, (BOARD_SIZE + 15, y_offset))
        y_offset += 35
        
        # Captured pieces
        pygame.draw.line(self.screen, (200, 200, 200), (BOARD_SIZE + 10, y_offset), (WINDOW_WIDTH - 10, y_offset))
        y_offset += 10
        
        cap_title = self.font_small.render("Captured / पकड़े गए:", True, TEXT_COLOR)
        self.screen.blit(cap_title, (BOARD_SIZE + 15, y_offset))
        y_offset += 25
        
        # Draw captured white pieces (captured by black)
        if self.captured_white:
            cap_x = BOARD_SIZE + 15
            for piece in self.captured_white[:8]:
                piece_surface = self.piece_renderer.get_piece_surface(piece.symbol())
                if piece_surface:
                    small_surface = pygame.transform.scale(piece_surface, (25, 25))
                    self.screen.blit(small_surface, (cap_x, y_offset))
                    cap_x += 28
        y_offset += 30
        
        # Draw captured black pieces (captured by white)
        if self.captured_black:
            cap_x = BOARD_SIZE + 15
            for piece in self.captured_black[:8]:
                piece_surface = self.piece_renderer.get_piece_surface(piece.symbol())
                if piece_surface:
                    small_surface = pygame.transform.scale(piece_surface, (25, 25))
                    self.screen.blit(small_surface, (cap_x, y_offset))
                    cap_x += 28
        y_offset += 40
        
        # Move history
        pygame.draw.line(self.screen, (200, 200, 200), (BOARD_SIZE + 10, y_offset), (WINDOW_WIDTH - 10, y_offset))
        y_offset += 10
        
        hist_title = self.font_small.render("Moves / चालें:", True, TEXT_COLOR)
        self.screen.blit(hist_title, (BOARD_SIZE + 15, y_offset))
        y_offset += 25
        
        # Show last 10 moves
        moves_to_show = self.move_history[-20:]  # Last 20 half-moves (10 full moves)
        move_text = ""
        for i, move in enumerate(moves_to_show):
            start_idx = len(self.move_history) - len(moves_to_show)
            actual_idx = start_idx + i
            if actual_idx % 2 == 0:
                move_num = (actual_idx // 2) + 1
                move_text += f"{move_num}."
            move_text += f"{move} "
        
        # Word wrap move history
        words = move_text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font_tiny.size(test_line)[0] < INFO_PANEL_WIDTH - 30:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        
        for line in lines[-8:]:  # Show last 8 lines
            text = self.font_tiny.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (BOARD_SIZE + 15, y_offset))
            y_offset += 18
        
        # Buttons at bottom
        y_offset = WINDOW_HEIGHT - 100
        
        # New Game button
        new_game_rect = pygame.Rect(BOARD_SIZE + 15, y_offset, INFO_PANEL_WIDTH - 30, 35)
        mouse_pos = pygame.mouse.get_pos()
        btn_color = BUTTON_HOVER if new_game_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, btn_color, new_game_rect, border_radius=5)
        btn_text = self.font_small.render("New Game / नया खेल", True, WHITE)
        text_rect = btn_text.get_rect(center=new_game_rect.center)
        self.screen.blit(btn_text, text_rect)
        
        y_offset += 45
        
        # Resign button
        resign_rect = pygame.Rect(BOARD_SIZE + 15, y_offset, INFO_PANEL_WIDTH - 30, 35)
        btn_color = BUTTON_HOVER if resign_rect.collidepoint(mouse_pos) else (180, 80, 80)
        pygame.draw.rect(self.screen, btn_color, resign_rect, border_radius=5)
        btn_text = self.font_small.render("Resign / हार मानें", True, WHITE)
        text_rect = btn_text.get_rect(center=resign_rect.center)
        self.screen.blit(btn_text, text_rect)
        
        return new_game_rect, resign_rect
    
    def draw_start_screen(self):
        """Draw the start screen for color selection"""
        self.screen.fill(WHITE)
        
        # Title
        title = self.font_large.render("Chess / शतरंज", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Player vs AI / खिलाड़ी बनाम AI", True, (100, 100, 100))
        sub_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 130))
        self.screen.blit(subtitle, sub_rect)
        
        # Instructions
        inst = self.font_small.render("Choose your color / अपना रंग चुनें:", True, TEXT_COLOR)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(inst, inst_rect)
        
        # White button with king piece
        white_rect = pygame.Rect(WINDOW_WIDTH // 2 - 180, 250, 160, 140)
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (220, 220, 220) if white_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(self.screen, btn_color, white_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, white_rect, 3, border_radius=10)
        
        # Draw white king
        white_king = self.piece_renderer.get_piece_surface('K')
        if white_king:
            scaled_king = pygame.transform.scale(white_king, (80, 80))
            self.screen.blit(scaled_king, (white_rect.centerx - 40, white_rect.centery - 50))
        
        white_text = self.font_small.render("White / सफेद", True, TEXT_COLOR)
        text_rect = white_text.get_rect(center=(white_rect.centerx, white_rect.centery + 50))
        self.screen.blit(white_text, text_rect)
        
        # Black button with king piece
        black_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, 250, 160, 140)
        btn_color = (60, 60, 60) if black_rect.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(self.screen, btn_color, black_rect, border_radius=10)
        
        # Draw black king
        black_king = self.piece_renderer.get_piece_surface('k')
        if black_king:
            scaled_king = pygame.transform.scale(black_king, (80, 80))
            self.screen.blit(scaled_king, (black_rect.centerx - 40, black_rect.centery - 50))
        
        black_text = self.font_small.render("Black / काला", True, WHITE)
        text_rect = black_text.get_rect(center=(black_rect.centerx, black_rect.centery + 50))
        self.screen.blit(black_text, text_rect)
        
        # Instructions at bottom
        inst1 = self.font_small.render("Click on a piece to select, then click destination", True, (100, 100, 100))
        inst_rect1 = inst1.get_rect(center=(WINDOW_WIDTH // 2, 480))
        self.screen.blit(inst1, inst_rect1)
        
        inst2 = self.font_small.render("मोहरे पर क्लिक करें, फिर गंतव्य पर क्लिक करें", True, (100, 100, 100))
        inst_rect2 = inst2.get_rect(center=(WINDOW_WIDTH // 2, 510))
        self.screen.blit(inst2, inst_rect2)
        
        # Piece legend
        y_pos = 560
        legend_text = self.font_tiny.render("Pieces / मोहरे:", True, TEXT_COLOR)
        self.screen.blit(legend_text, (WINDOW_WIDTH // 2 - 200, y_pos))
        
        pieces_info = [('K', 'King/राजा'), ('Q', 'Queen/रानी'), ('R', 'Rook/हाथी'), 
                       ('B', 'Bishop/ऊंट'), ('N', 'Knight/घोड़ा'), ('P', 'Pawn/प्यादा')]
        x_pos = WINDOW_WIDTH // 2 - 200
        y_pos += 25
        for piece_char, name in pieces_info:
            piece_surface = self.piece_renderer.get_piece_surface(piece_char)
            if piece_surface:
                small_surface = pygame.transform.scale(piece_surface, (30, 30))
                self.screen.blit(small_surface, (x_pos, y_pos))
                name_text = self.font_tiny.render(name, True, TEXT_COLOR)
                self.screen.blit(name_text, (x_pos + 35, y_pos + 8))
                x_pos += 120
                if x_pos > WINDOW_WIDTH - 150:
                    x_pos = WINDOW_WIDTH // 2 - 200
                    y_pos += 35
        
        return white_rect, black_rect
    
    def draw_promotion_dialog(self):
        """Draw promotion piece selection dialog"""
        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 350
        dialog_height = 180
        dialog_x = (WINDOW_WIDTH - dialog_width) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=10)
        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=10)
        
        # Title
        title = self.font_medium.render("Promote Pawn / प्यादा पदोन्नति", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, dialog_y + 30))
        self.screen.blit(title, title_rect)
        
        # Piece options
        pieces = ['Q', 'R', 'B', 'N'] if self.board.turn == chess.WHITE else ['q', 'r', 'b', 'n']
        piece_rects = []
        
        for i, piece in enumerate(pieces):
            x = dialog_x + 30 + i * 75
            y = dialog_y + 70
            rect = pygame.Rect(x, y, 65, 80)
            
            mouse_pos = pygame.mouse.get_pos()
            bg_color = (200, 200, 200) if rect.collidepoint(mouse_pos) else (240, 240, 240)
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=5)
            
            piece_surface = self.piece_renderer.get_piece_surface(piece)
            if piece_surface:
                scaled = pygame.transform.scale(piece_surface, (55, 55))
                self.screen.blit(scaled, (rect.centerx - 27, rect.centery - 35))
            
            piece_rects.append((rect, piece.upper()))
        
        return piece_rects
    
    def get_square_from_pos(self, pos: Tuple[int, int]) -> Optional[int]:
        """Convert screen position to chess square"""
        x, y = pos
        if x >= BOARD_SIZE:
            return None
        
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        
        if self.user_is_white:
            return chess.square(col, 7 - row)
        else:
            return chess.square(7 - col, row)
    
    def evaluate_position(self, board: chess.Board) -> int:
        """Evaluate the current board position"""
        if board.is_checkmate():
            return -20000 if board.turn == chess.WHITE else 20000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            value = PIECE_VALUES[piece.piece_type]
            pos_value = self.get_position_value(piece, square, board)
            
            if piece.color == chess.WHITE:
                score += value + pos_value
            else:
                score -= value + pos_value
        
        # Mobility bonus
        mobility = len(list(board.legal_moves))
        if board.turn == chess.WHITE:
            score += mobility * 5
        else:
            score -= mobility * 5
        
        return score
    
    def get_position_value(self, piece, square, board=None):
        """Get positional value for a piece on a square"""
        piece_type = piece.piece_type
        
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
            target_board = board if board is not None else self.board
            if len(target_board.piece_map()) <= 10:
                return KING_END_GAME_TABLE[square]
            else:
                return KING_MIDDLE_GAME_TABLE[square]
        
        return 0
    
    def minimax(self, board: chess.Board, depth: int, alpha: int, beta: int, 
                maximizing: bool) -> Tuple[int, Optional[chess.Move]]:
        """Minimax algorithm with Alpha-Beta pruning"""
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None
        
        best_move = None
        legal_moves = list(board.legal_moves)
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
                    break
            
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
                    break
            
            return min_eval, best_move
    
    def get_ai_move(self) -> Optional[chess.Move]:
        """Get the best move for AI"""
        ai_is_white = not self.user_is_white
        maximizing = ai_is_white
        
        _, best_move = self.minimax(
            self.board, 
            self.search_depth, 
            float('-inf'), 
            float('inf'), 
            maximizing
        )
        
        return best_move
    
    def make_move(self, move: chess.Move):
        """Make a move on the board"""
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            if captured_piece.color == chess.WHITE:
                self.captured_white.append(captured_piece)
            else:
                self.captured_black.append(captured_piece)
        
        san_move = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san_move)
        self.last_move = move
        self.selected_square = None
        self.legal_moves_for_selected = []
        
        # Check game status
        self.check_game_over()
    
    def check_game_over(self):
        """Check if the game is over"""
        if self.board.is_checkmate():
            winner = "Black / काला" if self.board.turn == chess.WHITE else "White / सफेद"
            self.game_over = True
            self.game_result = f"Checkmate! {winner} wins!"
            self.status_message = "शह और मात!"
        elif self.board.is_stalemate():
            self.game_over = True
            self.game_result = "Stalemate! Draw!"
            self.status_message = "गतिरोध! ड्रॉ!"
        elif self.board.is_insufficient_material():
            self.game_over = True
            self.game_result = "Draw - Insufficient material"
            self.status_message = "अपर्याप्त सामग्री"
        elif self.board.is_check():
            self.status_message = "Check! / शह!"
        else:
            self.status_message = ""
    
    def handle_click(self, pos: Tuple[int, int]) -> Optional[chess.Move]:
        """Handle mouse click on the board"""
        square = self.get_square_from_pos(pos)
        if square is None:
            return None
        
        piece = self.board.piece_at(square)
        
        # Check if user can move
        is_user_turn = (self.board.turn == chess.WHITE and self.user_is_white) or \
                      (self.board.turn == chess.BLACK and not self.user_is_white)
        
        if not is_user_turn:
            return None
        
        # If a piece is already selected
        if self.selected_square is not None:
            # Check if clicking on a legal move destination
            for move in self.legal_moves_for_selected:
                if move.to_square == square:
                    return move
            
            # Deselect if clicking on same square
            if square == self.selected_square:
                self.selected_square = None
                self.legal_moves_for_selected = []
                return None
        
        # Select a new piece
        if piece and piece.color == self.board.turn:
            self.selected_square = square
            self.legal_moves_for_selected = [m for m in self.board.legal_moves if m.from_square == square]
        else:
            self.selected_square = None
            self.legal_moves_for_selected = []
        
        return None
    
    def new_game(self):
        """Start a new game"""
        self.board = chess.Board()
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.selected_square = None
        self.legal_moves_for_selected = []
        self.last_move = None
        self.game_started = False
        self.game_over = False
        self.game_result = ""
        self.status_message = ""
    
    def run(self):
        """Main game loop"""
        running = True
        promotion_move = None
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        pos = pygame.mouse.get_pos()
                        
                        # Handle promotion dialog
                        if promotion_move:
                            piece_rects = self.draw_promotion_dialog()
                            for rect, piece_type in piece_rects:
                                if rect.collidepoint(pos):
                                    # Create promotion move
                                    promo_piece = {'Q': chess.QUEEN, 'R': chess.ROOK, 
                                                  'B': chess.BISHOP, 'N': chess.KNIGHT}[piece_type]
                                    final_move = chess.Move(promotion_move.from_square, 
                                                          promotion_move.to_square, 
                                                          promotion=promo_piece)
                                    self.make_move(final_move)
                                    promotion_move = None
                                    break
                            continue
                        
                        # Handle start screen
                        if not self.game_started:
                            white_rect, black_rect = self.draw_start_screen()
                            if white_rect.collidepoint(pos):
                                self.user_is_white = True
                                self.game_started = True
                            elif black_rect.collidepoint(pos):
                                self.user_is_white = False
                                self.game_started = True
                            continue
                        
                        # Handle info panel buttons
                        if pos[0] >= BOARD_SIZE:
                            new_game_rect = pygame.Rect(BOARD_SIZE + 15, WINDOW_HEIGHT - 100, INFO_PANEL_WIDTH - 30, 35)
                            resign_rect = pygame.Rect(BOARD_SIZE + 15, WINDOW_HEIGHT - 55, INFO_PANEL_WIDTH - 30, 35)
                            
                            if new_game_rect.collidepoint(pos):
                                self.new_game()
                                continue
                            elif resign_rect.collidepoint(pos) and not self.game_over:
                                winner = "AI / कंप्यूटर"
                                self.game_over = True
                                self.game_result = f"You resigned! {winner} wins!"
                                self.status_message = "आपने हार मान ली!"
                                continue
                        
                        # Handle board clicks
                        if not self.game_over and not self.ai_thinking:
                            move = self.handle_click(pos)
                            if move:
                                # Check if it's a pawn promotion
                                piece = self.board.piece_at(move.from_square)
                                if piece and piece.piece_type == chess.PAWN:
                                    to_rank = chess.square_rank(move.to_square)
                                    if to_rank == 7 or to_rank == 0:
                                        promotion_move = move
                                        continue
                                
                                self.make_move(move)
            
            # Draw everything
            if not self.game_started:
                self.draw_start_screen()
            else:
                self.draw_board()
                self.draw_pieces()
                self.draw_info_panel()
                
                if promotion_move:
                    self.draw_promotion_dialog()
            
            pygame.display.flip()
            
            # AI move (after user's turn)
            if self.game_started and not self.game_over and not self.ai_thinking and not promotion_move:
                is_ai_turn = (self.board.turn == chess.WHITE and not self.user_is_white) or \
                            (self.board.turn == chess.BLACK and self.user_is_white)
                
                if is_ai_turn:
                    self.ai_thinking = True
                    # Draw "thinking" message
                    self.draw_board()
                    self.draw_pieces()
                    self.draw_info_panel()
                    pygame.display.flip()
                    
                    # Get and make AI move
                    ai_move = self.get_ai_move()
                    if ai_move:
                        self.make_move(ai_move)
                    
                    self.ai_thinking = False
        
        pygame.quit()


def main():
    """Main function to start the game"""
    game = ChessGameGUI()
    game.run()


if __name__ == "__main__":
    main()
