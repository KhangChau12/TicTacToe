class TicTacToe {
    constructor() {
        this.board = Array(9).fill(null);
        this.currentPlayer = 'X'; // Player always goes first as X
        this.gameOver = false;
        this.winner = null;
        this.boardElement = document.getElementById('board');
        this.statusElement = document.getElementById('status');
        this.aiThinking = false;
        this.difficulty = 3; // Default difficulty
        this.difficultyInfo = {};
        
        // Statistics
        this.stats = {
            wins: parseInt(localStorage.getItem('ttt_wins') || 0),
            draws: parseInt(localStorage.getItem('ttt_draws') || 0),
            losses: parseInt(localStorage.getItem('ttt_losses') || 0)
        };
        
        // Update statistics display
        this.updateStats();
        
        // Create the board
        this.setupBoard();
        
        // Set up event listeners
        document.getElementById('new-game').addEventListener('click', () => this.resetGame(false));
        document.getElementById('ai-first').addEventListener('click', () => this.resetGame(true));
        
        // Set up difficulty slider
        const difficultySlider = document.getElementById('difficulty-slider');
        difficultySlider.value = this.difficulty;
        difficultySlider.addEventListener('input', (e) => {
            this.difficulty = parseInt(e.target.value);
            this.updateDifficultyDescription();
        });
        
        // Load difficulty information from API
        this.loadDifficultyInfo();
        
        // Hide loading screen after short delay to ensure everything is loaded
        setTimeout(() => {
            document.getElementById('loading').style.display = 'none';
        }, 1000);
    }
    
    async loadDifficultyInfo() {
        try {
            const response = await fetch('/api/difficulty-info');
            this.difficultyInfo = await response.json();
            this.updateDifficultyDescription();
        } catch (error) {
            console.error('Unable to load difficulty information:', error);
            // Fallback if unable to load
            this.difficultyInfo = {
                "1": { name: "Easy", description: "AI makes many mistakes and only looks 1 move ahead." },
                "2": { name: "Medium", description: "AI occasionally makes mistakes and looks 3 moves ahead." },
                "3": { name: "Hard", description: "AI rarely makes mistakes and looks 5 moves ahead." },
                "4": { name: "Expert", description: "AI doesn't make mistakes and looks 7 moves ahead." },
                "5": { name: "Invincible", description: "Perfect AI, cannot be defeated." }
            };
            this.updateDifficultyDescription();
        }
    }
    
    updateDifficultyDescription() {
        const descElem = document.getElementById('difficulty-description');
        const info = this.difficultyInfo[this.difficulty];
        if (info) {
            descElem.textContent = `${info.name}: ${info.description}`;
        }
    }
    
    setupBoard() {
        this.boardElement.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            cell.addEventListener('click', (e) => this.handleCellClick(e));
            this.boardElement.appendChild(cell);
        }
        this.updateStatus();
    }
    
    resetGame(aiFirst) {
        this.board = Array(9).fill(null);
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.winner = null;
        this.aiThinking = false;
        
        // Update interface
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.textContent = '';
            cell.className = 'cell';
        });
        
        this.boardElement.classList.remove('ai-thinking');
        this.updateStatus();
        
        // If AI goes first
        if (aiFirst) {
            this.currentPlayer = 'O';
            this.makeAIMove();
        }
    }
    
    handleCellClick(event) {
        if (this.gameOver || this.aiThinking || this.currentPlayer !== 'X') return;
        
        const index = event.target.dataset.index;
        if (this.board[index] !== null) return;
        
        // Update board with player's move
        this.makeMove(index);
        
        // Check if game over
        if (!this.gameOver) {
            // AI's turn
            this.currentPlayer = 'O';
            this.updateStatus();
            this.makeAIMove();
        }
    }
    
    makeMove(index) {
        this.board[index] = this.currentPlayer;
        const cell = document.querySelector(`.cell[data-index="${index}"]`);
        cell.textContent = this.currentPlayer;
        cell.classList.add(this.currentPlayer);
        
        // Check game state
        this.checkGameState();
    }
    
    checkGameState() {
        // Winning patterns
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Vertical
            [0, 4, 8], [2, 4, 6]             // Diagonal
        ];
        
        // Check each winning pattern
        for (const pattern of winPatterns) {
            const [a, b, c] = pattern;
            if (this.board[a] && this.board[a] === this.board[b] && this.board[a] === this.board[c]) {
                this.endGame(this.board[a]);
                return;
            }
        }
        
        // Check for draw
        if (!this.board.includes(null)) {
            this.endGame(null);
            return;
        }
        
        // Switch players
        this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
    }
    
    endGame(winner) {
        this.gameOver = true;
        this.winner = winner;
        
        // Update statistics
        if (winner === 'X') {
            this.stats.wins++;
            localStorage.setItem('ttt_wins', this.stats.wins);
        } else if (winner === 'O') {
            this.stats.losses++;
            localStorage.setItem('ttt_losses', this.stats.losses);
        } else {
            this.stats.draws++;
            localStorage.setItem('ttt_draws', this.stats.draws);
        }
        
        this.updateStats();
        this.updateStatus();
        
        // Add winner animation
        if (winner) {
            this.boardElement.classList.add('winner-animation');
            setTimeout(() => {
                this.boardElement.classList.remove('winner-animation');
            }, 1000);
        }
    }
    
    updateStats() {
        document.getElementById('wins').textContent = this.stats.wins;
        document.getElementById('draws').textContent = this.stats.draws;
        document.getElementById('losses').textContent = this.stats.losses;
    }
    
    updateStatus() {
        if (this.gameOver) {
            if (this.winner === 'X') {
                this.statusElement.textContent = 'You Won! 🎉';
                this.statusElement.style.backgroundColor = 'rgba(0, 230, 118, 0.2)';
                this.statusElement.style.borderLeft = '4px solid var(--secondary-color)';
            } else if (this.winner === 'O') {
                this.statusElement.textContent = 'AI Won! 🤖';
                this.statusElement.style.backgroundColor = 'rgba(255, 23, 68, 0.2)';
                this.statusElement.style.borderLeft = '4px solid var(--accent-color)';
            } else {
                this.statusElement.textContent = 'Draw! 🤝';
                this.statusElement.style.backgroundColor = 'rgba(255, 152, 0, 0.2)';
                this.statusElement.style.borderLeft = '4px solid #ff9800';
            }
        } else {
            if (this.currentPlayer === 'X') {
                this.statusElement.textContent = 'Your Turn';
                this.statusElement.style.backgroundColor = 'rgba(41, 98, 255, 0.2)';
                this.statusElement.style.borderLeft = '4px solid var(--primary-color)';
            } else {
                this.statusElement.textContent = 'AI Thinking...';
                this.statusElement.style.backgroundColor = 'rgba(156, 39, 176, 0.2)';
                this.statusElement.style.borderLeft = '4px solid #9c27b0';
            }
        }
    }
    
    // Call API to get AI's move
    async makeAIMove() {
        if (this.gameOver) return;
        
        this.aiThinking = true;
        this.boardElement.classList.add('ai-thinking');
        
        try {
            // Call API with board information and difficulty
            const response = await fetch('/api/ai-move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    board: this.board,
                    difficulty: this.difficulty
                }),
            });
            
            if (!response.ok) {
                throw new Error('Unable to get AI move');
            }
            
            const data = await response.json();
            
            // Make the move
            this.makeMove(data.move);
            
            // Switch players
            this.currentPlayer = 'X';
            
            this.aiThinking = false;
            this.boardElement.classList.remove('ai-thinking');
            this.updateStatus();
            
        } catch (error) {
            console.error('Error:', error);
            
            // Fallback: if API call fails, end AI's turn
            this.aiThinking = false;
            this.boardElement.classList.remove('ai-thinking');
            this.currentPlayer = 'X';
            this.updateStatus();
            alert('An error occurred while connecting to the AI. Please try again.');
        }
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    const game = new TicTacToe();
});
