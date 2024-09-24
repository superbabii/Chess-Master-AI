from flask import Flask, request, jsonify
from lczero.backends import Weights, Backend, GameState
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

weights_path = "weights/744706.pb.gz"
w = Weights(weights_path)
backend = Backend(weights=w)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    fen = data.get('fen')

    if not fen:
        return jsonify({"error": "FEN not provided"}), 400

    try:
        game_state = GameState(fen=fen)
        input_data = game_state.as_input(backend)
        output_tuple = backend.evaluate(input_data)
        evaluation = output_tuple[0].q()

        # Get move probabilities
        move_probs = list(zip(game_state.moves(), output_tuple[0].p_softmax(*game_state.policy_indices())))
        best_move = max(move_probs, key=lambda x: x[1])[0]

        # Split best_move into 'from' and 'to' for highlighting
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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
