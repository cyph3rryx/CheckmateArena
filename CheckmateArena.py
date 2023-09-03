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

    # Initialize the chess engine
    engine = chess.engine.SimpleEngine.popen_uci("D:\\Hacking\\Projects\\Chess Fight\\stockfish\\stockfish-windows-x86-64-avx2.exe")

    # Check if the directory exists
    if not os.path.exists("D:\\Hacking\\Projects\\Chess Fight"):
        os.makedirs("D:\\Hacking\\Projects\\Chess Fight")

    # File name as the current date and time
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

    # Open the file to record the game
    with open("D:\\Hacking\\Projects\\Chess Fight\\" + filename, "w") as file:
        # Game loop
        while not board.is_game_over():
            # Display the board with improved UI
            print_board(board)

            # Let the engine decide a move
            start = time.time()
            result = engine.play(board, chess.engine.Limit(time=0.1))
            end = time.time()

            # Make the move
            board.push(result.move)

            # Write the move and the score to the file
            info = engine.analyse(board, chess.engine.Limit(time=0.1))
            file.write(f"Move: {result.move} Score: {info['score']} Time: {end - start}\n")

    # Print game result
    result = board.result()
    if result == '1-0':
        print("White won the game")
    elif result == '0-1':
        print("Black won the game")
    else:
        print("The game was a draw")

    # Close the engine
    engine.quit()

if __name__ == "__main__":
    main()
