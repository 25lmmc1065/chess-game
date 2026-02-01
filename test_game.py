#!/usr/bin/env python3
"""
Test script to verify chess game modules work correctly
"""

import sys
import chess

# Test imports
print("Testing imports...")
try:
    from chess_ai import ChessAI
    print("✓ chess_ai imported successfully")
except ImportError as e:
    print(f"✗ Failed to import chess_ai: {e}")
    sys.exit(1)

try:
    import pygame
    print("✓ pygame imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pygame: {e}")
    sys.exit(1)

# Test AI engine
print("\nTesting AI engine...")
try:
    ai = ChessAI(search_depth=3)
    board = chess.Board()
    
    # Get AI move
    move = ai.get_best_move(board, ai_is_white=True)
    if move and move in board.legal_moves:
        print(f"✓ AI generated valid move: {board.san(move)}")
    else:
        print("✗ AI failed to generate valid move")
        sys.exit(1)
    
    # Test evaluation
    eval_score = ai.evaluate_position(board)
    print(f"✓ Position evaluation: {eval_score}")
    
    # Test minimax
    score, best_move = ai.minimax(board, 2, float('-inf'), float('inf'), True)
    print(f"✓ Minimax search completed: score={score}, move={board.san(best_move) if best_move else None}")
    
except Exception as e:
    print(f"✗ AI engine test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test chess logic
print("\nTesting chess logic...")
try:
    board = chess.Board()
    
    # Test basic moves
    e4 = chess.Move.from_uci("e2e4")
    board.push(e4)
    print(f"✓ Move e2-e4 executed")
    
    e5 = chess.Move.from_uci("e7e5")
    board.push(e5)
    print(f"✓ Move e7-e5 executed")
    
    # Test game state detection
    if not board.is_game_over():
        print("✓ Game state detection working")
    
    print(f"✓ Move history: {[move.uci() for move in board.move_stack]}")
    
except Exception as e:
    print(f"✗ Chess logic test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test pygame initialization (headless)
print("\nTesting pygame (headless mode)...")
try:
    import os
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    print("✓ Pygame initialized successfully")
    
    # Try to create a surface
    screen = pygame.display.set_mode((800, 600))
    print("✓ Display surface created")
    
    # Test font
    font = pygame.font.Font(None, 36)
    text = font.render("Test", True, (255, 255, 255))
    print("✓ Font rendering works")
    
    pygame.quit()
    print("✓ Pygame cleaned up")
    
except Exception as e:
    print(f"⚠ Pygame test warning (expected in headless environment): {e}")

print("\n" + "="*50)
print("All critical tests passed! ✓")
print("The chess game is ready to run.")
print("="*50)
print("\nTo play the game, run:")
print("  python main.py")
