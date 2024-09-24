import React, { useState, useEffect } from 'react';
import { Chess } from 'chess.js';
import { Chessboard } from 'react-chessboard';
import Swal from 'sweetalert2';
import './ChessGame.css';

const ChessGame = () => {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState(game.fen());
  const [history, setHistory] = useState([]);
  const [gameOver, setGameOver] = useState(false);
  const [status, setStatus] = useState('Game in progress');
  const [bestMove, setBestMove] = useState(null);

  // Fetch evaluation from backend
  const evaluatePosition = async (currentFen) => {
    try {
      const response = await fetch('http://localhost:5000/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fen: currentFen }),
      });

      if (response.ok) {
        const data = await response.json();
        setBestMove(data.best_move);
      } else {
        Swal.fire({
          title: 'Error',
          text: 'Failed to evaluate the position.',
          icon: 'error',
        });
      }
    } catch (error) {
      console.error(error);
      Swal.fire({
        title: 'Error',
        text: 'An error occurred during evaluation.',
        icon: 'error',
      });
    }
  };

  // Trigger evaluation when FEN changes
  useEffect(() => {
    if (!gameOver) {
      evaluatePosition(fen);
    }
  }, [fen]);

  // Check game status after each move
  useEffect(() => {
    if (game.isGameOver()) {
      setGameOver(true);
      if (game.isCheckmate()) {
        setStatus(`Checkmate! ${game.turn() === 'w' ? 'Black' : 'White'} wins.`);
        Swal.fire({
          title: 'Checkmate!',
          text: `${game.turn() === 'w' ? 'Black' : 'White'} wins the game.`,
          icon: 'success',
          confirmButtonText: 'New Game',
        }).then(() => resetGame());
      } else if (game.isDraw()) {
        setStatus('Draw!');
        Swal.fire({
          title: 'Draw!',
          text: 'The game ended in a draw.',
          icon: 'info',
          confirmButtonText: 'New Game',
        }).then(() => resetGame());
      } else if (game.isStalemate()) {
        setStatus('Stalemate!');
        Swal.fire({
          title: 'Stalemate!',
          text: 'The game ended in a stalemate.',
          icon: 'info',
          confirmButtonText: 'New Game',
        }).then(() => resetGame());
      }
    } else {
      setStatus(`Turn: ${game.turn() === 'w' ? 'White' : 'Black'}`);
    }
  }, [history, game]);

  // Handle piece movement
  const onPieceDrop = (sourceSquare, targetSquare) => {
    try {
      const move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: 'q',
      });

      if (move === null) {
        throw new Error('Illegal move');
      }

      // Update FEN, game state, and history
      setFen(game.fen());
      setHistory(game.history({ verbose: true }));
    } catch (error) {
      console.error(error.message);
      Swal.fire({
        title: 'Invalid Move',
        text: error.message,
        icon: 'error',
        confirmButtonText: 'Try Again',
      });
    }
  };

  // Reset the game
  const resetGame = () => {
    const newGame = new Chess();
    setGame(newGame);
    setFen(newGame.fen());
    setHistory([]);
    setGameOver(false);
    setStatus('Game in progress');
    setBestMove(null);
  };

  // Render move history
  const renderMoveHistory = () => {
    return history.map((move, index) => (
      <div key={index} className="move">
        {index % 2 === 0 ? `${Math.floor(index / 2) + 1}. ` : ''} {move.san}
      </div>
    ));
  };

  // Highlight squares for the best move and draw arrows
  const customSquareStyles = {
    ...(bestMove ? { [bestMove.from]: { backgroundColor: 'rgba(0, 255, 0, 0.4)' } } : {}),
    ...(bestMove ? { [bestMove.to]: { backgroundColor: 'rgba(255, 0, 0, 0.4)' } } : {}),
  };

  // Draw an arrow for the best move
  const customArrows = bestMove ? [[bestMove.from, bestMove.to]] : [];

  return (
    <div className="chess-game-container">
      <div className="top-section">
        <div className="fen-output">
          <h2>Current FEN: </h2>
          <p>{fen}</p>
        </div>
        <div className="best-move">
          <h2>Best Move: </h2>
          <p>{(bestMove?.from || 'unknown')}{(bestMove?.to || 'unknown')}</p>
        </div>
        <button className="reset-button" onClick={resetGame}>
          Reset Game
        </button>
      </div>
      <div className="game-status">
        <h2>{status}</h2>
      </div>
      <div className="main-section">
        <div className="board-section">
          <Chessboard
            position={fen}
            onPieceDrop={onPieceDrop}
            customSquareStyles={customSquareStyles} // Use customSquareStyles for highlighting
            customArrows={customArrows} // Use customArrows for drawing the arrow
          />
        </div>
        <div className="info-section">
          <div className="move-history">
            <h2>Move History:</h2>
            {renderMoveHistory()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChessGame;
