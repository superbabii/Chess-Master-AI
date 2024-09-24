# Chess Master AI

![Simple Prototype](simple-prototype.mp4)

**Chess Master AI** is a web application that integrates a powerful chess engine, **Lc0**, with a user-friendly interface to evaluate chess positions. The project uses a React frontend and a Flask backend, with Lc0 acting as the backend engine for evaluating both FEN and move sequences.

## Features

- **Evaluate Chess Positions:** Input a series of chess moves or a FEN string, and the backend will evaluate the position using Lc0.
- **LLM-Powered Analysis (Optional):** Receive detailed analysis, alternative suggestions, and insights from a Large Language Model (LLM).
- **Interactive Chessboard:** Visualize moves and positions on a chessboard using the React frontend.

## Requirements

### Backend

- Python 3.8+
- Flask
- Lc0 (Leela Chess Zero)
- TensorFlow (used by Lc0)
- Optional: OpenAI API (or any other LLM provider)
- Gunicorn (for production)

### Frontend

- Node.js (v14+ recommended)
- React
- Axios (for API requests)
- React-Chessboard (or similar chessboard library)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/superbabii/Chess-Master-AI.git
cd ChessMasterAI
```

### 2. Backend Setup

1. Create a virtual environment and install Python dependencies:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Download the Lc0 weights and place them in the `backend/weights/` directory. You can find Lc0 network weights at [Lc0 weights files storage](https://storage.lczero.org/files).

3. Set up your LLM API (optional) by registering for the OpenAI API (or any other LLM service) and setting the API key in an environment variable:

```bash
export OPENAI_API_KEY=your-api-key
```

4. Run the Flask server:

```bash
flask run
```

This will start the backend on `http://127.0.0.1:5000/`.

### 3. Frontend Setup

1. Install Node.js and dependencies:

```bash
cd frontend
npm install
```

2. Start the React development server:

```bash
npm start
```

This will start the React application on `http://localhost:3000/`.

### 4. API Endpoints

- **Evaluate Chess Position:**

  `POST /evaluate`

  This endpoint evaluates a chess position based on either a series of chess a FEN string. 

  **Request:**

  ```json
  {
    "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"   // Optional, for FEN
  }
  ```

  **Response:**

  ```json
  {
    "message": "Position evaluated successfully",
    "input": {...},  // Raw input details
    "evaluation": {
      "score": 0.32,  // Example evaluation score from the engine
      "best_move": "e2e4",  // Optional best move if applicable
      "analysis": "The opening move controls the center."  // Optional LLM analysis if enabled
    }
  }
  ```

## LLM Configuration (Optional)

You can enhance the chess evaluation by integrating an LLM to provide natural language explanations. If LLM analysis is enabled, responses will include explanations and alternative suggestions.

The backend integrates the LLM via API calls. Ensure you have set up the following environment variables:

- **`OPENAI_API_KEY`**: The API key for OpenAI (or equivalent LLM service).
- **`LLM_PROVIDER`**: If using a different LLM service, specify the provider here (e.g., "openai").

In the backend, LLM analysis is added to the evaluation routes:

```python
# In app.py
@app.route('/evaluate', methods=['POST'])
def evaluate_position():
    data = request.json
    fen = data.get('fen')
    moves = data.get('moves')
    
    if fen:
        engine_output = engine.evaluate_fen(fen=fen)
    elif moves:
        engine_output = engine.evaluate_moves(moves=moves)
    else:
        return jsonify({"error": "FEN or Moves are required"}), 400
    
    # Optional LLM call
    analysis = llm.analyze_position(fen or moves) if llm else None
    
    return jsonify({
        "message": "Position evaluated successfully",
        "input": engine_output,
        "evaluation": {
            "score": engine_output["score"],
            "best_move": engine_output.get("best_move"),
            "analysis": analysis
        }
    })
```

## Usage

1. Open the React app in the browser at `http://localhost:3000/`.
2. Use the interface to input chess moves or FEN positions.
3. The evaluated position and board state will be displayed on the chessboard.
4. Optional: Get detailed analysis from the LLM if enabled.

## Deployment

For production, you can run the backend with Gunicorn:

```bash
gunicorn -w 4 app:app
```

And build the frontend for production:

```bash
npm run build
```

Host both the frontend and backend using services like Heroku, AWS, or any other cloud provider.

## Troubleshooting

- **Error: `Lc0 weights not found`**  
  Ensure you’ve placed the Lc0 weights file in the correct `backend/weights/` directory.

- **CORS Issues**  
  If the frontend cannot communicate with the backend, ensure CORS is properly configured on the backend, especially for production.

- **LLM Errors (Optional)**  
  If you encounter errors with LLM responses, ensure your API key is set correctly and that the API call limits are not exceeded.

## Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues, please open an issue on GitHub.

## License

This project is licensed under the MIT License.
