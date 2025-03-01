# Minimax Tic-Tac-Toe AI

A web-based Tic-Tac-Toe game with an unbeatable AI that uses the Minimax algorithm with Alpha-Beta pruning.

![Tic Tac Toe Game](https://via.placeholder.com/800x400?text=Tic+Tac+Toe+Minimax+AI)

## Features

- Beautiful, responsive UI with smooth animations
- 5 difficulty levels, from Easy to Invincible
- Player statistics tracking (wins, draws, losses)
- Optimized Minimax algorithm with Alpha-Beta pruning
- Option to let AI go first

## How It Works

This game uses the Minimax algorithm with Alpha-Beta pruning, a recursive algorithm used for decision-making in game theory. The AI evaluates all possible moves by:

1. Simulating all possible future board states
2. Assigning scores to each state (-10 for loss, 0 for draw, +10 for win)
3. Choosing the move that leads to the maximum score for the AI
4. Using Alpha-Beta pruning to optimize the search process

At the highest difficulty level, the AI is unbeatable, but lower difficulty levels introduce random errors to make the game more accessible.

## Local Development

### Prerequisites

- Python 3.8 or higher
- Flask
- NumPy

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tictactoe-minimax.git
   cd tictactoe-minimax
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:8000`

## Deployment

This project is configured for easy deployment on Render. See the [deployment guide](DEPLOYMENT.md) for instructions.

## Project Structure

```
tictactoe-minimax/
├── static/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── game.js
├── app.py
├── requirements.txt
└── wsgi.py
```

## License

MIT License
