from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import json
import os
import random
import time

app = Flask(__name__, static_folder='static')

class MinimaxAgent:
    """Agent using Minimax algorithm with Alpha-Beta pruning"""
    
    def __init__(self, player=-1, difficulty=3):
        """
        Initialize Minimax Agent.
        
        Args:
            player: 1 for X, -1 for O
            difficulty: Difficulty level 1-5, affects search depth and error rate
        """
        self.player = player  # 1 for X, -1 for O
        self.difficulty = difficulty
        
        # Maximum depth based on difficulty
        self.max_depth = min(9, difficulty * 2 - 1)  # 1: depth 1, 3: depth 5, 5: depth 9
        
        # Random error rate (%)
        self.error_rate = max(0, 20 - difficulty * 5)  # 1: 15%, 2: 10%, 3: 5%, 4+: 0%
    
    def evaluate_board(self, board):
        """
        Evaluate board state from current player's perspective.
        
        Returns:
            10 if AI wins, -10 if opponent wins, 0 if draw or ongoing
        """
        # Check rows
        for i in range(3):
            if abs(np.sum(board[i, :])) == 3:
                return 10 if board[i, 0] == self.player else -10
        
        # Check columns
        for i in range(3):
            if abs(np.sum(board[:, i])) == 3:
                return 10 if board[0, i] == self.player else -10
        
        # Check main diagonal
        if abs(np.sum(np.diag(board))) == 3:
            return 10 if board[0, 0] == self.player else -10
        
        # Check anti-diagonal
        if abs(np.sum(np.diag(np.fliplr(board)))) == 3:
            return 10 if board[0, 2] == self.player else -10
        
        # Draw or ongoing
        return 0
    
    def minimax(self, board, depth, alpha, beta, is_maximizing, current_player):
        """
        Minimax algorithm with Alpha-Beta pruning.
        
        Args:
            board: Board state
            depth: Current depth
            alpha, beta: Alpha-Beta pruning bounds
            is_maximizing: True if maximizing, False if minimizing
            current_player: Current player (1 or -1)
            
        Returns:
            Score of the best state
        """
        # Check for terminal state or max depth
        score = self.evaluate_board(board)
        
        # If game over or max depth reached
        if score != 0 or depth == 0 or 0 not in board:
            return score
        
        # If leaf node and depth at least 3, can return eval with heuristic
        if depth <= 3 and 0 not in board:
            return score
        
        # Find valid moves
        valid_moves = []
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    valid_moves.append((i, j))
        
        # If maximizing (AI)
        if is_maximizing:
            best_score = -float('inf')
            for move in valid_moves:
                i, j = move
                # Create copy of board to try move
                new_board = board.copy()
                new_board[i, j] = current_player
                
                # Recurse with next player
                score = self.minimax(new_board, depth-1, alpha, beta, False, -current_player)
                best_score = max(score, best_score)
                
                # Update alpha
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta pruning
                
            return best_score
        
        # If minimizing (opponent)
        else:
            best_score = float('inf')
            for move in valid_moves:
                i, j = move
                # Create copy of board to try move
                new_board = board.copy()
                new_board[i, j] = current_player
                
                # Recurse with next player
                score = self.minimax(new_board, depth-1, alpha, beta, True, -current_player)
                best_score = min(score, best_score)
                
                # Update beta
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha pruning
                
            return best_score
    
    def get_best_move(self, board, current_player=None):
        """
        Find best move based on Minimax algorithm.
        
        Args:
            board: Board state
            current_player: Current player (default is self.player)
            
        Returns:
            Best move as tuple (i, j)
        """
        if current_player is None:
            current_player = self.player
        
        # Simulate random error based on difficulty
        if random.random() < self.error_rate / 100:
            # If error, choose random move
            valid_moves = []
            for i in range(3):
                for j in range(3):
                    if board[i, j] == 0:
                        valid_moves.append((i, j))
            
            if valid_moves:
                return random.choice(valid_moves)
        
        # Find valid moves
        valid_moves = []
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    valid_moves.append((i, j))
        
        # If no valid moves, return None
        if not valid_moves:
            return None
        
        # If only one move, return it
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        # If first move and AI goes first, choose corner or center
        if np.sum(np.abs(board)) == 0 and current_player == self.player:
            best_first_moves = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]
            return random.choice(best_first_moves)
        
        # If second move and AI goes second, some special strategies
        if np.sum(np.abs(board)) == 1 and current_player == self.player:
            # If opponent chooses corner, best is center
            if board[0, 0] != 0 or board[0, 2] != 0 or board[2, 0] != 0 or board[2, 2] != 0:
                if board[1, 1] == 0:
                    return (1, 1)
            
            # If opponent chooses center, best is corner
            if board[1, 1] != 0:
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                available_corners = [c for c in corners if board[c[0], c[1]] == 0]
                if available_corners:
                    return random.choice(available_corners)
        
        # Perform Minimax with Alpha-Beta pruning
        best_score = -float('inf')
        best_move = valid_moves[0]  # Default is first move
        
        # Try each move and choose the one with highest score
        for move in valid_moves:
            i, j = move
            # Create copy of board to try move
            new_board = board.copy()
            new_board[i, j] = current_player
            
            # Call minimax with next player
            # Depth based on empty cells (fewer cells, higher depth)
            empty_cells = len(valid_moves)
            adaptive_depth = min(self.max_depth, empty_cells + 1)
            
            score = self.minimax(new_board, adaptive_depth, -float('inf'), float('inf'), False, -current_player)
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

# Initialize AI with default difficulty (can be adjusted from frontend)
ai_agents = {
    "1": MinimaxAgent(difficulty=1),
    "2": MinimaxAgent(difficulty=2),
    "3": MinimaxAgent(difficulty=3),
    "4": MinimaxAgent(difficulty=4),
    "5": MinimaxAgent(difficulty=5)
}
default_ai = ai_agents["3"]  # Default difficulty is 3

# Convert board data from frontend to numpy format
def convert_board_to_numpy(board_array):
    board = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            if board_array[index] == 'X':
                board[i, j] = 1
            elif board_array[index] == 'O':
                board[i, j] = -1
    return board

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/api/ai-move', methods=['POST'])
def ai_move():
    data = request.json
    board_array = data.get('board', [None] * 9)
    difficulty = str(data.get('difficulty', 3))
    
    # Convert board to numpy format
    board = convert_board_to_numpy(board_array)
    
    # Get AI based on difficulty
    ai = ai_agents.get(difficulty, default_ai)
    
    # Add artificial delay to create "thinking" feeling
    artificial_delay = min(1.0, 0.2 * int(difficulty))  # Higher difficulty, longer "thinking"
    time.sleep(artificial_delay)
    
    # Get best move
    move = ai.get_best_move(board)
    
    if move is None:
        return jsonify({'error': 'No valid moves'})
    
    # Convert (i, j) to 0-8 index for frontend
    move_index = move[0] * 3 + move[1]
    
    return jsonify({'move': int(move_index)})

@app.route('/api/difficulty-info', methods=['GET'])
def difficulty_info():
    """Return information about difficulty levels"""
    difficulties = {
        "1": {
            "name": "Easy",
            "description": "AI makes many mistakes and only looks 1 move ahead.",
            "win_rate": "~85%"
        },
        "2": {
            "name": "Medium",
            "description": "AI occasionally makes mistakes and looks 3 moves ahead.",
            "win_rate": "~90%"
        },
        "3": {
            "name": "Hard",
            "description": "AI rarely makes mistakes and looks 5 moves ahead.",
            "win_rate": "~95%"
        },
        "4": {
            "name": "Expert",
            "description": "AI doesn't make mistakes and looks 7 moves ahead.",
            "win_rate": "~99%"
        },
        "5": {
            "name": "Invincible",
            "description": "Perfect AI, cannot be defeated.",
            "win_rate": "100%"
        }
    }
    return jsonify(difficulties)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
