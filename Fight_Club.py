import chess
import chess.engine
import datetime
import os
import time
import numpy as np

PIECE_ART = {
    None: " . ",
    chess.PAWN: " ♟ ",
    chess.KNIGHT: " ♞ ",
    chess.BISHOP: " ♝ ",
    chess.ROOK: " ♜ ",
    chess.QUEEN: " ♛ ",
    chess.KING: " ♚ ",
}

# Function to display the chessboard with styling
def print_board(board):
    print("   a  b  c  d  e  f  g  h")
    print(" +------------------------+")
    for rank in range(8):
        print(f"{8 - rank}|", end="")
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            if piece:
                symbol = PIECE_ART[piece.piece_type]
                if piece.color == chess.BLACK:
                    print(f"\033[30m{symbol}\033[0m", end="")  # Black pieces in black
                else:
                    print(f"\033[37m{symbol}\033[0m", end="")  # White pieces in white
            else:
                print(PIECE_ART[None], end="")
        print("|")
    print(" +------------------------+")
    print("   a  b  c  d  e  f  g  h")

# Function to convert the chess board to a matrix
def board_to_matrix(board):
    pgn = board.epd()
    foo = []
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for r in rows:
        foo2 = []
        for p in r:
            if p.isdigit():
                for i in range(0, int(p)):
                    foo2.append('.')
            else:
                foo2.append(p)
        foo.append(foo2)
    return np.array(foo)

# Function to convert a move to a pair of coordinates
def move_to_coordinates(move):
    return [move.from_square, move.to_square]

def main():
    # Initialize the chess board
    board = chess.Board()

    # Define engine paths and time controls
    stockfish_path = "\\path\\to\\stockfish-engine"
    komodo_path = "\\path\\to\\komodo-engine"
    
    stockfish_time = 1.0  # Adjust time control as needed (in seconds)
    komodo_time = 1.0   # Adjust time control as needed (in seconds)

    # Initialize the chess engines
    stockfish_engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    komodo_engine = chess.engine.SimpleEngine.popen_uci(komodo_path)

    # Check if the directory exists
    save_folder = "\\path\\to\\folder"  # Specify the folder
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # File name as the current date and time
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"  # Use .txt extension

    # Open the file to record the game
    with open(os.path.join(save_folder, filename), "w") as file:
        # Game loop
        while not board.is_game_over():
            # Display the board with improved UI
            print_board(board)

            if board.turn == chess.WHITE:
                engine = stockfish_engine
                current_time = stockfish_time
            else:
                engine = komodo_engine
                current_time = komodo_time

            # Let the engine decide a move
            start = time.time()
            legal_moves = list(board.legal_moves)  # Get the list of legal moves
            if legal_moves:
                result = engine.play(board, chess.engine.Limit(time=current_time))  # Limit the time per move
                end = time.time()

                # Make the move
                board.push(result.move)

                # Convert the board and the move to their matrix representations
                board_matrix = board_to_matrix(board)
                move_coordinates = move_to_coordinates(result.move)

                # Write the preprocessed data to the file
                file.write(f"Board: {board_matrix.tolist()} Move: {move_coordinates}\n")
            else:
                print("No legal moves left. Game over.")
                break

        # Print game result
        result = board.result()
        if result == '1-0':
            print("White won the game")
            file.write("White won the game\n")
        elif result == '0-1':
            print("Black won the game")
            file.write("Black won the game\n")
        else:
            print("The game was a draw")
            file.write("The game was a draw\n")

    # Close the engines
    stockfish_engine.quit()
    komodo_engine.quit()

if __name__ == "__main__":
    main()
