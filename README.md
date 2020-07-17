
# SHAPE 2020 - Advnaced Computer Science
## Adversarial Serach / Game Playing

### Introduction

In this project you will implement an AI player for the game Othello, also known as Reversi. For the rules of this game see here: [https://en.wikipedia.org/wiki/Reversi](https://en.wikipedia.org/wiki/Reversi). Our version of the game differs from these rules in one minor point: The game ends as soon as one of the players has no legal moves left.

The project consists of the following 5 files: 

-   othello_gui.py - Contains a simple graphical user interface (GUI) for Othello.
-   othello_game.py - Contains the game "manager", which stores the current game state and communicates with different player AIs.
-   othello_shared.py - Functions for computing legal moves, captured disks, and successor game states. These are shared between the game manager, the GUI and the AI players.
-   randy_ai.py - Randy is an "AI" player that randomly selects a legal move.
-   YOURUNI_ai.py - This is the scaffolding code you will use to build your AI player. Rename this file by replacing YOURUNI with your actual UNI.

#### Game State Representation
Each game state contains two pieces of information: The current player and the current disks on the board. Throughout our implementation, Player 1 (dark) is represented using the integer 1, and Player 2 (light) is represented using the integer 2.

The board is represented as a a tuple of tuples. The inner tuple represents each row of the board. Each entry in the rows is either an empty square (integer 0), a dark disk (integer 1) or a light disk (integer 2). For example, the 8x8 initial state looks like this:
```
((0, 0, 0, 0, 0, 0, 0, 0),  
 (0, 0, 0, 0, 0, 0, 0, 0),  
 (0, 0, 0, 0, 0, 0, 0, 0),  
 (0, 0, 0, 2, 1, 0, 0, 0),  
 (0, 0, 0, 1, 2, 0, 0, 0),  
 (0, 0, 0, 0, 0, 0, 0, 0),  
 (0, 0, 0, 0, 0, 0, 0, 0),  
 (0, 0, 0, 0, 0, 0, 0, 0))
```

#### Getting Started
Run the Othello GUI, <code>python othello_gui.py</code>, which should bring up a game window. By default, both players are human players, taking turn.

The GUI can take one or two AI programs as command line parameters. When only one of them is specified, you will play against the AI (you will be player 1, dark): `$python othello_gui.py randy_ai.py` Play against Randy to develop a better understanding of how the game works and what strategies can give you an advantage.  
  
When two AIs are specified you can watch them play against each other: `$python othello_gui.py randy_ai.py randy_ai.py`.

The GUI is rather minimalistic, so you need to close the window and then restart to play a new game.

(On some systems, you will get an error message when the game is trying to run randy_ai. In that case, your system is probably configured to use the command "python3" to call python 3. To fix this problem change the line `subprocess.Popen(["python", filename]...` to `subprocess.Popen(["python3", filename]...)` in othello_game.py.)

#### Communication between the Game Host and the AI
This is a technical detail that you can skip if you are not interested. Functions for communicating with the game manager are provided as part of the scaffolding code.

The AI and the Game Manager / GUI will run in different Python interpreters. The Game Manager / GUI will spawn a child process for each AI player. This makes it easier for the game manager to let the AI process time out and also makes sure that, if the AI crashes, the game manager can keep running. To communicate with the child process, the game manager uses pipes. Essentially, the game manager reads from the AI's standard output and writes to the AI's standard input. The two programs follow a precise protocol to communicate:

-   The AI sends a string to identify itself. For example, randy_ai sends "Randy". You should come up with a fun name for your AI.
-   The game manager sends back "1" or "2", indicating if the AI plays dark or light.
-   Then the AI sits and waits for input form the game manager. When it is the AI's turn, the game manager will send two lines: The current score, for example "SCORE 2 2" and the game board (a Python tuple converted to string). The game manager then waits for the AI to respond with a move, for example "4 3".
-   At the end of the game, the game master sends the final score, for example "FINAL 33 31".

#### Time Constraints
Your AI player will be expected to make a move within 10 seconds. If no move has been selected, the AI loses the game. This time constraint does not apply for human players.

You may change the time constraint by editing line 34 in othello_game.py: TIMEOUT = 10

However, we will run your AI with a timeout of 10 seconds during grading and for the Othello competition.

### **Part I. Minimax**

First, change line 139 in othello_gui.py `game = OthelloGameManager(dimension=8)`to `game = OthelloGameManager(dimension=4)`. This will run Othello on a 4x4 board. This restriction makes the game somewhat trivial: it is easy even for human players to think ahead to the end of the game. When both players play optimally, the player who goes second always wins. However, the default Minimax algorithm, without a depth limit, takes too long even on a 6x6 board.

Write the function `compute_utility(board, color)` that computes the utility of a final game board state (in the format described above). The utility is the number of disks of player `color` minus the number of disks of the opponent. Hint: The function `get_score(board)` returns a tuple (number of dark disks, number of light disks).

Then, implement the method `select_move_minimax(board, color)` that selects the action that leads to the state with the highest minimax value. The parameters of the function are the current board (in the format described above) and the color for the AI player, integer 1 for dark and 2 for light. The return value should be a (column, row) tuple, representing the move. Hints:

-   Implement Minimax recursively by writing two functions `minimax_max_node(board, color)` and `minimax_min_node(board, color)`.
-   Use the `get_possible_moves(board, color)` function in othello_shared.py, which returns a list of (column, row) tuples representing the legal moves for player color.
-   Use the `play_move(board, color, move)` function in othello_shared.py, which computes the successor board state that results from player color playing move (a (column, row) tuple).
-   Pay attention to which player should make a move for min nodes and max nodes.

You should now be able to play against your AI on a 4x4 board or have your AI play against the random AI.

### **Part II. α-β Pruning **

The simple Minimax approach becomes infeasible for boards larger than 4x4. Write the function `select_move_alphabeta(board, color)` which computes the best move using α-β-pruning. The parameters and return values are the same as for minimax.

Write recursive functions `alphabeta_min_node(board, color, alpha, beta)` and `alphabeta_max_node(board,color, alpha, beta)`.

In the main function of YOURUNI_ai.py change the line

`movei, movej = select_move_minimax(board, color)`

to

`movei, movej = select_move_alphabeta(board, color)`.

This should speed up decisions for the AI, but still not enough to be able to play larger boards than 4x4.

α-β-pruning works better if nodes that lead to a better utility are explored first. In the α-β-pruning functions, order successor states according to the following heuristic: nodes for which the #AI player's disks - #opponent's disk is highest should be explored first. Note that this is the same as the utility function, and it is okay to call the ultity function to compute this value. This should provide another small speed-up.

### **Part V. Depth Limit and Heuristic Evaluation **

So far we could only play on a trivial 4x4 board. Modify your α-β-pruning functions so that the algorithm only explores a limited number of levels, rather than the entire search tree. The function signatures should be `alphabeta_min_node(board, color, alpha, beta, level, limit)` and `alphabeta_max_node(board, color, alpha, beta, level, limit)`, where level is the current ply and limit is the total number of plies that should be explored. Instead of using the true utility at the final board states, we will use a *heuristic evaluation function* that is defined in the same way as the utility (i.e. you can simply call the utility function as before to estimate the quality of a state). You can then experiment with different heuristics!

Now switch back to an 8x8 board and experiment with the depth limit. What is the maximum number of plies you can safely evaluate in 10 seconds?

Taken together, these steps should give you an AI player that is challenging to play against.


Here are some ideas for further improvements:

-   Come up with a better node-ordering function.
-   Come up with a better evaluation function.
-   Instead of a fixed depth limit, use iterative deepening and a timer to maximize the number of levels you can explore in 10 seconds.
-   Use a different strategy in the opening, mid-game, and end-game.
-   Use a pattern database of common board states (you may include **one data file of at most 500kb** with your entry).

