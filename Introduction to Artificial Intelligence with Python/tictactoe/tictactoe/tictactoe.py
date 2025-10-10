"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None
countMoves = 0

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    The player function should take a board state as input, and return which player’s turn it is (either X or O).
    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).

    Minimax + Alpha-Beta Pruning
    """
    global countMoves
    # initial game state = X gets first move
    if board == initial_state():
        return X

    # game is already over
    if(terminal(board)):
        return None

    XMoves = 0
    OMoves = 0

    for row in board:
        XMoves += row.count(X)
        OMoves += row.count(O)

    if XMoves <= OMoves:
        return X
    else:
        return O
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    The actions function should return a set of all of the possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.
    """
    # if terminal board, return empty set
    if terminal(board):
        return set()
    #check each row and cell of each board for EMPTY cells and collect & return them as possible actions
    return returnEmptyCells(board)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
    If action is not a valid action for the board, your program should raise an exception.
    The returned board state should be the board that would result from taking the original input board,
    and letting the player whose turn it is make their move at the cell indicated by the input action.
    Importantly, the original board should be left unmodified: since Minimax will ultimately require considering
    many different board states during its computation.
    This means that simply updating a cell in board itself is not a correct implementation of the result function.
    You’ll likely want to make a deep copy of the board first before making any changes.
    """
    # Create a deep copy of the board
    boardCopy = [row.copy()for row in board]

    # Check if the action is valid
    if not verifyMove(board, action):
        raise Exception("Invalid action")
    # Apply the action to the copied board
    boardCopy[action[0]][action[1]] = player(board)
    return boardCopy

def verifyMove(board, action):
    #check if the action is valid
    if action in returnEmptyCells(board):
        return True
    return False

def winner(board):
    """
    Returns the winner of the game, if there is one.

    The winner function should accept a board as input, and return the winner of the board if there is one.
    If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    You may assume that there will be at most one winner
    (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
    If there is no winner of the game
    (either because the game is in progress, or because it ended in a tie), the function should return None.
    """
    #check each cell of the board for a winner
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    The terminal function should accept a board as input, and return a boolean value indicating whether the game is over.
    If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return True.
    Otherwise, the function should return False if the game is still in progress.
    """
    # check if there is a winner or if there are any EMPTY cells left
    if (winner(board) != None) | (returnEmptyCells(board) == set()):
        return True

    return False

def returnEmptyCells(board):
    possibleActions=set()
    #check each row and cell of each board for EMPTY cells and collect & return them as possible actions
    for rowIndex, row in enumerate(board):
        for columnIndex, cell in enumerate(row):
            if cell == EMPTY:
                possibleActions.add((rowIndex, columnIndex))
    return possibleActions


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    The utility function should accept a terminal board as input and output the utility of the board.
    If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
    You may assume utility will only be called on a board if terminal(board) is True.
    """
    if(winner(board) == X):
        return 1
    elif(winner(board) == O):
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    The minimax function should take a board as input, and return the optimal move for the player to move on that board.
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.
    """
   
    currentPlayer = player(board)
    # determines the maximum value for the maximizing player (X)
    def maxValue(board):
        if(terminal(board)):
            return (utility(board),set())
        bestValue = -math.inf
        bestAction = set()
        possibleActions=actions(board)
        for possibleAction in possibleActions:
            checkedBoard=result(board, possibleAction)
            checkedValue =  minValue(checkedBoard)[0]
            
            if checkedValue > bestValue:
                bestValue = checkedValue
                bestAction = possibleAction
        return (bestValue,bestAction)
    # determines the minimum value for the minimizing player (O)
    def minValue(board):
        if(terminal(board)):
            return (utility(board),set())
        bestValue = math.inf
        bestAction = set()
        possibleActions=actions(board)
        for possibleAction in possibleActions:
            checkedBoard=result(board, possibleAction)
            checkedValue= maxValue(checkedBoard)[0]

            if checkedValue < bestValue:
                bestValue = checkedValue
                bestAction = possibleAction
        return (bestValue,bestAction)

    bestAction = set()
    if currentPlayer == X:
        bestAction=maxValue(board)[1]
    else:
         bestAction= minValue(board)[1]
    return bestAction


