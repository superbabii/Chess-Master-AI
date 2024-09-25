from flask import Flask, request, jsonify
from lczero.backends import Weights, Backend, GameState
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize LCZero backend with weights
weights_path = "weights/744706.pb.gz"
w = Weights(weights_path)
backend = Backend(weights=w)

# OpenAI API Key (ensure the key is stored securely in environment variables)
openai.api_key = "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"


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    fen = data.get('fen')

    if not fen:
        return jsonify({"error": "FEN not provided"}), 400

    try:
        # Generate the GameState and get evaluation
        game_state = GameState(fen=fen)
        input_data = game_state.as_input(backend)
        output_tuple = backend.evaluate(input_data)
        evaluation = output_tuple[0].q()

        # Get move probabilities and best move
        move_probs = list(zip(game_state.moves(), output_tuple[0].p_softmax(*game_state.policy_indices())))
        best_move = max(move_probs, key=lambda x: x[1])[0]  # Get the best move based on probability

        # Parse best move into 'from' and 'to'
        best_move_from = best_move[:2]
        best_move_to = best_move[2:]

        return jsonify({
            "evaluation": evaluation,
            "best_move": {
                "from": best_move_from,
                "to": best_move_to
            }
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred during evaluation: {str(e)}"}), 500


@app.route('/llm_chat', methods=['POST'])
def llm_chat():
    data = request.get_json()
    user_query = data.get('query', None)
    game_fen = data.get('fen', None)

    if user_query:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Use the new model family
                messages=[
                    {"role": "system", "content": "You are a chess expert."},
                    {"role": "user", "content": f"Answer this chess question: {user_query}"}
                ]
            )
            return jsonify({'response': response['choices'][0]['message']['content'].strip()})

        except Exception as e:
            app.logger.error(f"Error in user query LLM: {str(e)}")
            return jsonify({"error": f"LLM error: {str(e)}"}), 500

    if game_fen:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a chess expert."},
                    {"role": "user", "content": f"Describe the chess game with FEN {game_fen} and suggest the best moves."}
                ]
            )
            return jsonify({'response': response['choices'][0]['message']['content'].strip()})

        except Exception as e:
            app.logger.error(f"Error in FEN evaluation LLM: {str(e)}")
            return jsonify({"error": f"LLM error: {str(e)}"}), 500

    return jsonify({'error': 'Invalid input: Provide either query or FEN'}), 400


if __name__ == '__main__':
    app.run(debug=True)
