"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    score = None
    if board.check_win() != None:
        if board.check_win() == provided.DRAW:
            score = 0
        else:
            score = SCORES[ board.check_win() ]
        return(score, (-1,-1))
    else:
        respond = []
        for empty_squ in board.get_empty_squares():
            temp_board = board.clone()
            temp_board.move(empty_squ[0],empty_squ[1],player)
            result = mm_move(temp_board, provided.switch_player(player))
            respond.append((result[0], empty_squ)) 
        if len(respond) > 1:
            temp_score = [SCORES[player] * respond[num][0] for num in range(len(respond))]
            value = max(temp_score)
            max_index = temp_score.index(value)
            respond = [respond[max_index]]
        return respond[0]
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1];

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
