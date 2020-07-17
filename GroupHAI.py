
#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: YOUR NAME AND UNI 
"""

import random
import sys
import time
import othello_shared as os 
import math

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    Score = get_score(board) 
    Player1 = Score[0]
    Player2 = Score [1]

    return (Player1 - Player2)

def cornerpiece_heuristic(move): 
  if (move[0] == 0 and move[1] == 0): 
    return 3 
  elif (move[0] == 0 and move[1] == 6): 
    return 3 
  elif (move[0] == 6 and move[1] == 0): 
    return 3
  elif (move[0] == 6 and move[1] == 6): 
    return 3
  else: 
    return 0 

def nextToCornerpieceHeuristic(move): 
  if (move[0] == 2 and move[1] == 2): 
    return -2 
  elif (move[0] == 2 and move[1] == 5): 
    return -2
  elif (move[0] == 5 and move[1] == 2): 
    return -1
  elif (move[0] == 5 and move[0] == 5): 
    return -2 
  else: 
    return 0  

def weakMoves(move): 
  if (move[0] == 1 and move[1] == 2): 
    return -1
  elif (move[0] == 1 and move[1] == 5): 
    return -1
  elif (move[0] == 2 and move[1] == 1): 
    return -1 
  elif (move[0] == 5 and move[1] == 1): 
    return -1
  elif (move[0] == 6 and move[1] == 2): 
    return -1
  elif (move[0] == 6 and move[1] == 5): 
    return -1 
  elif (move[0] == 2 and move[1] == 6): 
    return -1
  else: 
    return 0


def mobilityHeuristic(board, move):
    new_board = os.play_move(board, 1, move[0], move[1])
    ai_moves = len(os.get_possible_moves(board, 2))
    player_moves = len(os.get_possible_moves(new_board, 1))
    return ai_moves - player_moves

############ MINIMAX ###############################
def minimax(board, depth, max_depth, is_max, color, cornerpiece, nextCornerpiece, mobility_score): 
  if depth == max_depth: 
    updated_score = compute_utility(board, color) + cornerpiece + nextCornerpiece + mobility_score


    return (None, updated_score)
  #game is over at this point
  else:
    moves = os.get_possible_moves(board, color)
    if len(moves) == 0: 
      updated_score = compute_utility(board, color) + cornerpiece - nextCornerpiece - mobility_score
      return (None, updated_score)
    else: 
      if is_max: 
        best_score = -math.inf
      else: 
        best_score = math.inf
      
      score_modifier = 0 
      for move in moves: 
        new_board = os.play_move(board, color, move[0], move [1])
        cornerpiece = cornerpiece_heuristic(move)
        if depth==0 and cornerpiece: 
          return (move, 10000)

        nextCornerpiece = nextToCornerpieceHeuristic(move)
        if depth==0 and nextCornerpiece: 
          score_modifier = -10000

        mobility_score = mobilityHeuristic(board, move)
        #score = os.get_score(board)
        dummymove, score = minimax(new_board, depth+1, max_depth, not is_max, color, cornerpiece, nextCornerpiece, mobility_score)
        score += score_modifier
        if is_max: 
          if best_score < score: 
            best_score = score
            best_move = move
        else:
          if best_score > score: 
            best_score = score
            best_move = move
            
      updated_score = best_score
      chosen_move = best_move
      return (chosen_move, best_score)

#================================================

def select_move_minimax(board, color):
  best_move, score = minimax(board, 0, 5, True, color, None, None, None)
  print(best_move, file=sys.stderr)
  return best_move
  

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta): 
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    return None


def select_move_alphabeta(board, color): 
    return 0,0 


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
