from lczero.backends import Weights, Backend, GameState

# Specify the path to the weights file
weights_path = "weights/744706.pb.gz"
w = Weights(weights_path)

available_backends = Backend.available_backends()
print(f"Available Backends: {available_backends}")

# Create backend
b = Backend(weights=w)

# Another GameState with FEN string and create input
fen = 'rnbqkb1r/pppp2pp/5n2/4pp2/4PP2/3B4/PPPP2PP/RNBQK1NR w KQkq - 1 4'
g_fen = GameState(fen=fen)
print(g_fen.as_string())
i2 = g_fen.as_input(b)

# Evaluate only this game state
o2_tuple = b.evaluate(i2)

# Since it's returning a tuple, extract the first element
o2 = o2_tuple[0]  # Unpacking the tuple to get the result

# Print evaluation
print(f"Evaluation for state (q): {o2.q()}")

# Get move probabilities
move_probs = list(zip(g_fen.moves(), o2.p_softmax(*g_fen.policy_indices())))
print("Move probabilities:")
for move, prob in move_probs:
    print(f"Move: {move}, Probability: {prob}")
