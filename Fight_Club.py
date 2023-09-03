import chess
import chess.engine
import datetime
import os
import time

# Define ASCII art for chess pieces
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
                    print(f"{symbol}", end="")
                else:
                    print(f"{symbol.upper()}", end="")
            else:
                print(PIECE_ART[None], end="")
        print("|")
    print(" +------------------------+")
    print("   a  b  c  d  e  f  g  h")

def main():
    # Initialize the chess board
    board = chess.Board()

    # Define engine paths and time controls
    stockfish_path = "K:\\Engines\\stockfish\\stockfish-windows-x86-64-avx2.exe"
    komodo_path = "K:\\Engines\\komodo-14\\Windows\\komodo-14.1-64bit.exe"
    
    stockfish_time = 0.1  # Adjust time control as needed (in seconds)
    komodo_time = 0.1    # Adjust time control as needed (in seconds)

    # Initialize the chess engines
    stockfish_engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    komodo_engine = chess.engine.SimpleEngine.popen_uci(komodo_path)

    # Check if the directory exists
    save_folder = "K:\\Projects\\chess-data"  # Specify the folder
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

                # Write the move and the time taken to the file
                file.write(f"Move: {result.move} Time: {end - start:.2f} seconds\n")
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
