# Chess Master AI

![Simple Prototype](simple-prototype.mp4)

**Chess Master AI** is a web application that integrates a powerful chess engine, Lc0, with a user-friendly interface to evaluate chess moves and positions. The project uses a React frontend and a Flask backend, with Lc0 acting as the backend engine for evaluating moves and FEN positions.

## Features

- **Evaluate Chess Moves:** Input a series of moves and have the backend evaluate the position.
- **Evaluate FEN Strings:** Submit a FEN (Forsyth-Edwards Notation) position and get an evaluation from the Lc0 engine.
- **Interactive Chessboard:** Visualize moves and positions on a chessboard using the React frontend.

## Requirements

### Backend

- Python 3.8+
- Flask
- Lc0 (Leela Chess Zero)
- TensorFlow (used by Lc0)
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

3. Run the Flask server:

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

- **Evaluate Moves:**

  `POST /evaluate_moves`

  **Request:**

  ```json
  {
    "moves": ["e2e4", "e7e5"]
  }
  ```

  **Response:**

  ```json
  {
    "message": "Moves evaluated successfully",
    "input": {...}
  }
  ```

- **Evaluate FEN:**

  `POST /evaluate_fen`

  **Request:**

  ```json
  {
    "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
  }
  ```

  **Response:**

  ```json
  {
    "message": "FEN evaluated successfully",
    "input": {...}
  }
  ```

## Usage

1. Open the React app in the browser at `http://localhost:3000/`.
2. Use the interface to input chess moves or FEN positions.
3. The evaluated moves and board state will be displayed on the chessboard.

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

## Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues, please open an issue on GitHub.

## License

This project is licensed under the MIT License.
