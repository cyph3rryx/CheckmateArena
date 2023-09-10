import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Entry
from stockfish import Stockfish
import chess
import chess.pgn
import threading
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import chess.svg
import cairosvg
import tkinter.ttk as ttk
import chess.polyglot

class ChessAnalyzer:
    def __init__(self, stockfish_path, opening_book_path):
        self.stockfish_path = stockfish_path
        self.opening_book_path = opening_book_path
        self.moves_info = []
        self.current_move = 0

        self.root = tk.Tk()
        self.root.title("Chess Analyzer")

        # Load the icon image (replace 'icon.png' with the path to your icon file)
        icon_img = PhotoImage(file='icon.png')
        self.root.iconphoto(False, icon_img)

        # Create GUI elements
        self.open_button = tk.Button(self.root, image=icon_img, command=self.open_pgn_file)
        self.open_button.pack()

        self.game_info_text = tk.StringVar()
        self.game_info_label = tk.Label(self.root, textvariable=self.game_info_text)
        self.game_info_label.pack()

        self.move_info_text = tk.StringVar()
        self.move_info_label = tk.Label(self.root, textvariable=self.move_info_text)
        self.move_info_label.pack()

        self.endgame_info_text = tk.StringVar()
        self.endgame_info_label = tk.Label(self.root, textvariable=self.endgame_info_text)
        self.endgame_info_label.pack()

        self.total_accuracy_text = tk.StringVar()
        self.total_accuracy_label = tk.Label(self.root, textvariable=self.total_accuracy_text)
        self.total_accuracy_label.pack()

        self.suspicious_info_text = tk.StringVar()
        self.suspicious_info_label = tk.Label(self.root, textvariable=self.suspicious_info_text, fg="red")
        self.suspicious_info_label.pack()

        self.next_button = tk.Button(self.root, text="Next Move", command=self.next_move)
        self.next_button.pack()

        self.previous_button = tk.Button(self.root, text="Previous Move", command=self.previous_move)
        self.previous_button.pack()

        self.loading_label = None

    def run(self):
        self.root.mainloop()

    def evaluate_position(self, board, time_limit=0.01):
        stockfish = Stockfish(self.stockfish_path)
        stockfish.set_fen_position(board.fen())
        best_move = stockfish.get_best_move_time(int(time_limit * 1000))
        evaluation = stockfish.get_evaluation()
        return best_move, evaluation

    def update_move_info(self, move_info):
        move_number, move, best_move, evaluation = move_info
        self.move_info_text.set(f"Move {move_number}: {move} | Best Move: {best_move} | Evaluation: {evaluation}")

        # Display the board
        svg = chess.svg.board(board=chess.Board(fen=board.fen()), lastmove=move)
        png = cairosvg.svg2png(bytestring=svg.encode('utf-8'))
        img = ImageTk.PhotoImage(Image.open(io.BytesIO(png)))
        self.board_label.config(image=img)
        self.board_label.image = img

    def open_pgn_file(self):
        pgn_file_path = filedialog.askopenfilename(filetypes=[("PGN Files", "*.pgn")])

        if pgn_file_path:
            self.loading_label = tk.Label(self.root, text="Loading...")
            self.loading_label.pack()

            threading.Thread(target=self.analyze_pgn, args=(pgn_file_path,)).start()

    def analyze_pgn(self, pgn_file_path):
        pgn = open(pgn_file_path)

        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            board = chess.Board()

            self.game_info_text.set(f"Result: {game.headers['Result']}\nOpening (ECO): {game.headers['ECO']}")

            for move_number, move in enumerate(game.mainline_moves(), start=1):
                board.push(move)
                best_move, evaluation = self.evaluate_position(board)
                self.moves_info.append((move_number, move, best_move, evaluation))

                # Display opening name
                with chess.polyglot.open_reader(self.opening_book_path) as reader:
                    opening = reader.find(board)
                    if opening:
                        self.opening_name_text.set(opening.move())

                if self.is_endgame(board):
                    self.endgame_info_text.set("Endgame started")

            total_accuracy = np.mean([100 if str(move[1]) == move[2] else max(0, 100 - abs(move[3]['value'])) for move in self.moves_info])
            self.total_accuracy_text.set(f"Total accuracy: {total_accuracy:.2f}%")

            if total_accuracy > 95:
                self.suspicious_info_text.set("Warning: The opponent might be cheating!")

        self.loading_label.destroy()
        self.update_move_info(self.moves_info[0])

# Replace "path_to_stockfish_executable" with the path to your Stockfish engine
app = ChessAnalyzer("D:\\Hacking\\Projects\\Chess Fight\\Engines\\stockfish\\stockfish-windows-x86-64-avx2.exe")
app.run()
