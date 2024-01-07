# Chess Bot 

## Overview

A Player vs Bot Chess game implemented in Python using the Pygame library. The bot uses a basic artificial intelligence algorithm to make moves.

## Installation

Pygame Installation

    pip install pygame

## Minimax Algorithm

The minimax algorithm is a recursive algorithm to find the best move possible that is used for chess bots. It navigates through a tree, assigning scores to each possible move while maximizesing the score for the current player (MAX) and minimizing the score for the opponent (MIN) at alternating depths. It backtracks through the tree, selecting moves that lead to the best possible outcome. Alpha-beta pruning has been implemented to optimize the algorithm by reducing unnecessary evaluations that cannot affect the final decision. The best move is the move with the highest score at the root node.

```python
    def Minimax(self, moves, d, alpha, beta, turn):
        global new_coordinates, piece_name, original_coordinates
        if d == 0:
            return turn * self.scoreBoard() 
        maxScore = -checkmate 
        for move in moves: 
            self.ifCastle()
            self.makeMove(move[2], move[3], move[0], move[1], move[4]) #move[0]/move[1] is old x and y coordinates
            self.checkCastle(move[4], move[2], move[3]) #move[2]/move[3] is the new x and y coordinates
            if self.ifCheck():
                self.Undo(move[0], move[1], move[4], move[5], move[2], move[3]) #move[4] is the moved piece and move[5] is captured piece
                continue
            self.white = not self.white
            nextmoves = self.allMoves() 
            score = -self.Minimax(nextmoves, d-1, -beta, -alpha, -turn) #minimax but for other side
            if score > maxScore:
                maxScore = score 
                if d == depth:
                    new_coordinates = (move[2], move[3]) #these variables contains the properities for the current best move found
                    piece_name = self.board[move[2]][move[3]]
                    original_coordinates = (move[0], move[1])
            self.Undo(move[0], move[1], move[4], move[5], move[2], move[3]) 
            self.white = not self.white
            if maxScore > alpha: #alpha beta pruning 
                alpha = maxScore 
            if alpha >= beta: #if alpha is higher than beta the function doesn't need to check the beta's path
                break #breaks out of the loop since it knows it won't find a higher score than alpha
        return maxScore
```

## Calculation of scores

### Piece
Each chess piece is assigned a numerical value based on its relative strength in the game.
Values:
* Pawn: 1
* Knight: 3
* Bishop: 3
* Rook: 5
* Queen: 9
* King: Infinite (9999 is used as it's unreachable)

### Position
The value of a piece is influenced by its position on the board. I've assigned my own numerical values to the positions for each piece based on how beneficial it is. In general, the squares closer to the center or the position where the piece can attack the most is the best. The king will typically want to stay at the back to avoid checkmate. 

```python
    def scoreBoard(self): #uses positional and piece values to calculate how good a move is
        piecevalue = {"k": 0, "q": 9, "r": 5, "n": 3, "b": 3, "p": 1} #value for each piece
        knightScores = [[1, 1, 1, 1, 1, 1, 1, 1], #below are values for each pieces positions
                        [1, 1, 2, 2, 2, 2, 1, 1],
                        [1, 2, 2, 3, 3, 2, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 2, 3, 3, 2, 2, 1],
                        [1, 1, 2, 2, 2, 2, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1]
                        ]
        bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4], 
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [4, 3, 2, 1, 1, 2, 3, 4]
                        ]
        queenScores = [[1, 1, 1, 3, 3, 1, 1, 1], 
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 1, 1, 3, 3, 1, 1, 1]
                       ]
        rookScores = [[4, 3, 4, 4, 4, 4, 3, 4], 
                      [4, 4, 4, 4, 4, 4, 4, 4],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [4, 4, 4, 4, 4, 4, 4, 4],
                      [4, 3, 4, 4, 4, 4, 3, 4]
                      ]
        whitepawnScores = [[8, 8, 8, 8, 8, 8, 8, 8], 
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [4, 4, 5, 5, 5, 5, 4, 4],
                           [2, 3, 4, 4, 4, 4, 3, 2],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 1, 2, 3, 3, 2, 2, 1],
                           [1, 1, 1, 0, 0, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0]
                           ]
        whitekingScores = [[1, 1, 1, 1, 1, 1, 1, 1], 
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [2, 1, 1, 1, 1, 1, 1, 2],
                           [2, 2, 1, 1, 1, 1, 2, 2],
                           [2, 2, 2, 1, 1, 2, 2, 2],
                           [3, 3, 2, 2, 2, 2, 3, 3],
                           [3, 5, 3, 3, 3, 5, 3, 3],
                           ]
        blackkingScores = [[3, 5, 3, 3, 3, 5, 3, 3], 
                           [3, 3, 2, 2, 2, 2, 3, 3],
                           [2, 2, 2, 1, 1, 2, 2, 2],
                           [2, 2, 1, 1, 1, 1, 2, 2],
                           [2, 1, 1, 1, 1, 1, 1, 2],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1]
                           ]
        blackpawnScores = [[0, 0, 0, 0, 0, 0, 0, 0], 
                           [1, 1, 1, 0, 0, 1, 1, 1],
                           [1, 1, 2, 3, 3, 2, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [2, 3, 4, 4, 4, 4, 3, 2],
                           [4, 4, 5, 5, 5, 5, 4, 4],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [8, 8, 8, 8, 8, 8, 8, 8]
                           ]
        positionScores = {"n": knightScores, "q": queenScores, "b": bishopScores, "r": rookScores, "bp": blackpawnScores, "wp": whitepawnScores,
                          "bk": blackkingScores, "wk": whitekingScores} 
        totalScore = 0
        positionScore = 0 
        if self.checkmate: 
            if self.white:
                return -checkmate
            else:
                return checkmate
        elif self.stalemate: 
            return stalemate
        for x in range(8):
            for y in range(8): 
                if self.board[x][y] != " ":
                    if self.board[x][y][1] == "n": 
                        positionScore = positionScores["n"][x][y] 
                    elif self.board[x][y][1] == "q":
                        positionScore = positionScores["q"][x][y]
                    elif self.board[x][y][1] == "b":
                        positionScore = positionScores["b"][x][y]
                    elif self.board[x][y][1] == "r":
                        positionScore = positionScores["r"][x][y]
                    elif self.board[x][y] == "wp":
                        positionScore = positionScores["wp"][x][y]
                    elif self.board[x][y] == "bp":
                        positionScore = positionScores["bp"][x][y]
                    elif self.board[x][y] == "wk":
                        positionScore = positionScores["wk"][x][y]
                    elif self.board[x][y] == "bk":
                        positionScore = positionScores["bk"][x][y]
                    if self.board[x][y][0] == "w": 
                        totalScore += piecevalue[self.board[x][y][1]] + positionScore*0.5 
                    elif self.board[x][y][0] == "b":
                        totalScore -= piecevalue[self.board[x][y][1]] + positionScore*0.5 
        return totalScore #returns total score. If total score is positive, it's winning for white and vice versa
```

## Meta

Max Oberhellman – maxoberhellman@gmail.com

Distributed under the MIT license. See LICENSE for more information.

https://github.com/moberhel/
