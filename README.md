# ♖ ♘ ♗ CheckmateArena  ♗ ♘ ♖

## Abstract

The CheckmateArena project revolves around developing an automated chess game that provides users with an immersive experience of watching two AI opponents play against each other. The game aims to record every move made by the AI players and present it to the user in text format upon completion. The project also includes enhancements to the terminal user interface to make it more visually appealing, resembling real chess pieces, accurate chess notations, and timers that record the time taken for each AI move.

## Introduction

Chess is a classic board game that has captivated players for centuries due to its complexity and strategic depth. With advancements in artificial intelligence and computer chess engines, it has become possible to create fully automated chess games where AI algorithms can play against each other, providing an opportunity for users to witness the strategies and tactics employed by these powerful AI players.

## Project Objectives

1. **Automated Chess Gameplay:** The project's core objective is to implement an automated chess game that allows two AI opponents to play against each other autonomously. Users will be able to observe the game's progression without actively participating.

2. **Move Recording:** The system will record every move made by the AI players throughout the game. This move history will be saved in a text file for reference, analysis, or review by the user.

3. **Enhanced Terminal UI:** The terminal user interface will be improved to provide a more visually appealing and immersive experience. Tangible chess piece symbols will be used, and the board will be displayed with accurate chess notations.

4. **Move Timer:** The system will include timers that record the time taken by each AI player to make their moves. This feature allows users to understand the game's pace and the AI opponents' time management skills.

## Workflow and Implementation for Chess Game with Stockfish Engine Integration

This code has a Python script that allows you to play chess against the Stockfish chess engine. It displays the chessboard with ASCII art, lets the engine decide the moves, and records the game to a file. Below is a detailed workflow and implementation of this code:

### Workflow

1. **Initialization:**
    - Import the necessary modules (`chess`, `chess.engine`, `time`) for chess game control, engine integration, and timing.
    - Define `PIECE_ART`, an ASCII art dictionary representing chess pieces.
    - Define a function `print_board` to display the chessboard with styling using the ASCII art.

2. **Main Function (`main`):**
    - Initialize the chessboard (`board`) and the chess engine (`engine`) by providing the path to the Stockfish engine executable.

3. **Game Loop:**
    - Open a file ("game.txt") to record the game moves.

4. **While Loop (Game in Progress):**
    - Display the chessboard using the `print_board` function, showing the game's current state.

5. **Engine Move Decision:**
    - Start measuring the time (`start`) for the engine to make a move.
    - Use the Stockfish engine (`engine.play`) to calculate the best move within a time limit (0.5 seconds).
    - Stop measuring time (`end`) after the engine makes a move.

6. **Make the Move:**
    - Push the move selected by the engine (`result.move`) onto the chessboard.

7. **Record Move and Score:**
    - Analyze the current board state (`engine.analyse`) to retrieve information about the move, such as the score.
    - Write the move, the engine's score, and the time taken for the engine's move to the file.

8. **Game Over Check:**
    - Continue the game loop until the game is over (`board.is_game_over()` returns True).

9. **Game Completion:**
    - After the game ends, close the engine using `engine.quit()`.

### Implementation

Here's how the code works:

- We initialize the chessboard (`board`) and the chess engine (`engine`) in the `main` function.
- We open a file ("game.txt") to record the game moves and results.
- In the game loop, we display the chessboard using the `print_board` function, which formats the board with ASCII art.
- The engine decides its move based on the current board state, taking a maximum of 0.5 seconds to decide.
- The selected move is executed on the chessboard.
- Move details, including the selected move, the engine's score for the move, and the time taken, are recorded in the game file.
- The loop continues until the game ends, and the engine is closed.

Make sure to provide the correct path to the Stockfish engine executable (`"K:\\Projects\\CheckmateArena\\Engines\\stockfish\\stockfish-windows-x86-64-avx2.exe"`) and ensure you have write permissions for the output file ("game.txt"). This code provides a simple way to play chess against the Stockfish engine in a text-based interface while recording the game's progress.

