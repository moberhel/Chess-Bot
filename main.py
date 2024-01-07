import pygame
from pygame.constants import MOUSEBUTTONDOWN
import random

class State():
    def __init__(self):
        self.board = [
            ["br","bn","bb","bk","bq","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wk","wq","wb","wn","wr"]
        ]
        self.white = True #who's turn it is
        self.wcastle = True 
        self.bcastle = True
        self.wqcastle = True 
        self.bqcastle = True
        self.wk = (7,3) 
        self.bk = (0,3) 
        self.checkmate = False 
        self.stalemate = False 

    def makeMove(self, nx, ny, ox, oy, p): 
        self.board[nx][ny] = p 
        self.board[ox][oy] = " " 
        if p == "wk":
            self.wk = (nx,ny) #if a king was moved for checking check
        elif p == "bk":
            self.bk = (nx,ny)
 
    def Error(self, x, y, display): 
        c = pygame.Color("red")
        pygame.draw.circle(display, c, ((x*50)+25,(y*50)+25), 15) 

    def specialMoves(self, p, x, y): #function for special situations like en passant, castle, pawn promotion
        self.checkCastle(p, x, y)
        if x == 0 and p == "wp": 
            self.pawnPromotion(x, y, p) 
        elif x == 7 and p == "bp":
            self.pawnPromotion(x, y, p)
        if p == "wp" and x+1 == 3 and self.board[x+1][y] == "bp":
            self.board[x+1][y] = " "
        if p == "bp" and x-1 == 4 and self.board[x-1][y] == "wp":
            self.board[x-1][y] = " "

    def checkCastle(self, p, x, y):
        if p == "wk":
            if self.wcastle and x == 7 and y == 5: 
                r1 = (7,7) #old coordinates of rook
                r2 = (7,4) #new coordiantes of rook
                self.makeMove(r2[0], r2[1], r1[0], r1[1], "wr") 
                self.wqcastle == False 
            elif self.wcastle and x == 7 and y == 1:
                r1 = (7,0)
                r2 = (7,2)
                self.makeMove(r2[0], r2[1], r1[0], r1[1], "wr")
                self.wcastle == False 
        elif p == "bk":
            if self.bcastle and x == 0 and y == 5: 
                r1 = (0,7)
                r2 = (0,4)
                self.makeMove(r2[0], r2[1], r1[0], r1[1], "br")
                self.bqcastle == False 
            elif self.bcastle and x == 0 and y == 1:
                r1 = (0,0)
                r2 = (0,2)
                self.makeMove(r2[0], r2[1], r1[0], r1[1], "br")
                self.bcastle == False 
        
    def Castle(self, r1, r2, p):
        if p[0] == "w": 
            self.board[r1[0]][r1[1]] = " " 
            self.board[r2[0]][r2[1]] = "wr" 
        else: 
            self.board[r1[0]][r1[1]] = " "
            self.board[r2[0]][r2[1]] = "br"
    
    def pawnPromotion(self, x, y, p):
        if p[0] == "w": 
                self.board[x][y] = "wq" 
        else: 
                self.board[x][y] = "bq"             

    def movePiece(self, moveapiece, display): 
        self.ifCastle() #checks every turn if the king moved for castling
        moves = [] #list that stores the possible moves the piece that's being moved
        if moveapiece.piece== " ":
            return
        newmove = (moveapiece.nx,moveapiece.ny) #what square the piece is being moved to 
        self.possibleMoves(moveapiece.piece, moveapiece.ox, moveapiece.oy, moves) 
        self.ifCheck() 
        if ((moveapiece.piece[0] == "w" and self.white == True) or (moveapiece.piece[0] == "b" and self.white == False)) and newmove in moves:
            cp = self.board[moveapiece.nx][moveapiece.ny] #opposing piece 
            self.makeMove(moveapiece.nx,moveapiece.ny, moveapiece.ox, moveapiece.oy, moveapiece.piece) 
            self.specialMoves(moveapiece.piece, moveapiece.nx, moveapiece.ny) 
            if self.ifCheck(): 
                self.Undo(moveapiece.ox, moveapiece.oy, moveapiece.piece, cp, moveapiece.nx, moveapiece.ny) 
                self.Error(moveapiece.ox, moveapiece.oy, display) 
                self.white = not self.white 
            self.white = not self.white  
        else: 
            self.Error(moveapiece.ox, moveapiece.oy, display)

    def possibleMoves(self, p, x, y, moves):
        if p[1] == "p": 
            self.Pawn(p,x,y,moves)
        elif p[1] == "n":
            self.Knight(p,x,y,moves)
        elif p[1] == "b":
            self.Bishop(p,x,y,moves)
        elif p[1] == "r":
            self.Rook(p,x,y,moves)
        elif p[1] == "q":
            self.Bishop(p,x,y,moves)
            self.Rook(p,x,y,moves)
        elif p[1] == "k":
            self.King(p,x,y,moves)

        
    def Pawn(self, p, x, y, moves): #possible moves for a pawn
        if p[0] == "w": 
            if x-1 >= 0 and self.board[x-1][y] == " ": 
                moves.append((x-1,y)) 
            if  x == 6 and self.board[x-2][y] == " " and self.board[x-1][y] == " ": 
                moves.append((x-2,y))
            for dy in (-1, 1): 
                ny = y + dy #
                nx = x - 1
                if 0 <= ny <= 7 and self.board[nx][ny][0] == "b": #
                    moves.append((nx, ny))
                if x == 3 and 0 <= ny <= 7 and self.board[x][ny] == "bp" and self.board[nx][ny] == " ": #en passant
                    moves.append((nx, ny))
        else: 
            if x+1 <= 7 and self.board[x+1][y] == " ":
                moves.append((x+1, y))
            if x == 1 and self.board[x+2][y] == " " and self.board[x+1][y] == " ":
                moves.append((x+2,y))
            for dy in (-1, 1): 
                ny = y + dy
                nx = x + 1 
                if 0 <= ny <= 7 and self.board[nx][ny][0] == "w":
                    moves.append((nx, ny))
                if x == 4 and 0 <= ny <= 7 and self.board[x][ny] == "wp" and self.board[nx][ny] == " ": #en passant
                    moves.append((nx, ny))

    def Knight(self, p, x, y, moves): #possible moves for a knight
        for (dx, dy) in [(1, -2), (1, 2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]: 
            nx = x + dx 
            ny = y + dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]:
                moves.append((nx,ny))
            else:
                pass

    def Rook(self, p, x, y, moves): #possible moves for a rook
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]: 
            for i in range(1, 8): 
                nx = x + dx*i 
                ny = y + dy*i
                if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]: 
                    moves.append((nx,ny))
                    if self.board[nx][ny][0] != " ": 
                        break
                else:
                    break 

    def Bishop(self, p, x, y, moves): #possible moves for a bishop
        for (dx, dy) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]: 
                for i in range(1, 8):
                    nx = x + dx*i
                    ny = y + dy*i
                    if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]: 
                        moves.append((nx,ny))
                        if self.board[nx][ny][0] != " ":
                            break
                    else:
                        break

    def King(self, p, x, y, moves): #possible moves for a king
        if p[0] == "w":
            if self.wqcastle and self.board[7][6] == " " and self.board[7][5] == " " and self.board[7][4] == " ":
                moves.append((7,5))
            if self.wcastle and self.board[7][1] == " " and self.board[7][2] == " ":
                moves.append((7,1))
        else:
            if self.bqcastle and self.board[0][6] == " " and self.board[0][5] == " " and self.board[0][4] == " ":
                moves.append((0,5))
            if self.bcastle and self.board[0][1] == " " and self.board[0][2] == " ":
                moves.append((0,1))
        for (dx, dy) in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]: 
            nx = x + dx
            ny = y + dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]:
                moves.append((nx,ny))
                if self.board[nx][ny][0] != " ":
                    pass
            else:
                pass

    def ifCastle(self): 
        if (self.board[7][3] != "wk" or self.board[7][0] != "wr"):
            self.wcastle = False #checks if king has moved for castle
        if (self.board[0][3] != "bk" or self.board[0][0] != "br"):
            self.bcastle = False
        if (self.board[7][3] != "wk" or self.board[7][7] != "wr"):
            self.wqcastle = False #checks if king has moved for castle
        if (self.board[0][3] != "bk" or self.board[0][7] != "br"):
            self.bqcastle = False
 
    def Undo(self, x, y, p, cp, nx, ny):
        if p == "wr" and x == 7 and y == 0:
            self.wcastle = True
        elif p == "br" and x == 0 and y == 0:
            self.bcastle = True
        elif p == "wr" and x == 7 and y == 7:
            self.wqcastle = True
        elif p == "br" and x == 0 and y == 7:
            self.bqcastle = True
        if p == "wk": #undos castle
            if x == 7 and y == 3:
                self.wcastle = True
                self.wqcastle = True
                if nx == 7 and ny == 5: 
                    r2 = (7,7) #new coordinates of rook
                    r1 = (7,4) #old coordiantes of rook
                    self.makeMove(r2[0], r2[1], r1[0], r1[1], "wr") 
                elif nx == 7 and ny == 1:
                    r2 = (7,0)
                    r1 = (7,2)
                    self.makeMove(r2[0], r2[1], r1[0], r1[1], "wr")
        elif p == "bk":
            if x == 0 and y == 3:
                self.bcastle = True
                self.bqcastle = True
                if nx == 0 and ny == 5: 
                    r2 = (0,7)
                    r1 = (0,4)
                    self.makeMove(r2[0], r2[1], r1[0], r1[1], "br")
                elif nx == 0 and ny == 1:
                    r2 = (0,0)
                    r1 = (0,2)
                    self.makeMove(r2[0], r2[1], r1[0], r1[1], "br")
        if p == "wk":
            self.wk = (x, y) #if a king was moved then the original coordinates go back to normal
        elif p == "bk":
            self.bk = (x, y)
        self.board[x][y] = p
        self.board[nx][ny] = cp 
    
    def undoEnpassant(self, p, encp, x, y):
        if p == "wp" and encp == "bp" and x+1 == 3 and self.board[x+1][y] == "":
            self.board[x+1][y] = " "
        if p == "bp" and encp == "wp" and x-1 == 4 and self.board[x-1][y] == "":
            self.board[x-1][y] = " "

    def ifCheck(self):  
        if self.white: 
            return self.ifCapturing(self.wk[0], self.wk[1]) 
        else: 
            return self.ifCapturing(self.bk[0], self.bk[1]) 
    
    def ifCapturing(self, x, y):
        self.white = not self.white #switches to opposing player's turn
        omove = self.allMoves() #finds all possible moves for opposing player
        self.white = not self.white #back to current player's turn
        for i in range(len(omove)): 
            if omove[i][2] == x and omove[i][3] == y: #if there's a possible move that attacks the player's king
                return True 
        return False

    def allMoves(self):
        allmoves = []
        if self.white == True:
            side = "w" 
        else:
            side = "b" 
        for y in range(8):
            for x in range(8): 
                piecemoves = []
                p = self.board[x][y] 
                if p[0] == side:
                    self.possibleMoves(p, x, y, piecemoves) 
                    for move in piecemoves: 
                        encp = "" 
                        if len(move) == 3:
                            encp = move[2] #specifically to track for the captured pawn in an en passant
                        allmoves.append((x, y, move[0], move[1], self.board[x][y], 
                        self.board[move[0]][move[1]], encp)) 
        return allmoves

    def ifCheckmate(self): 
        kingmoves = []
        if self.white:
            self.King("wk", self.wk[0], self.wk[1], kingmoves)
            p = "wk"
            ox = self.wk[0]
            oy = self.wk[1] 
        else:
            self.King("bk", self.bk[0], self.bk[1], kingmoves)
            p = "bk"
            ox = self.bk[0]
            oy = self.bk[1] 
        if self.ifCheck():
            if kingmoves != 0: 
                for i in range(len(kingmoves)-1, -1, -1): 
                    cp = self.board[kingmoves[i][0]][kingmoves[i][1]]
                    nx = kingmoves[i][0]
                    ny = kingmoves[i][1]
                    self.makeMove(nx, ny, ox, oy, p) 
                    if self.ifCheck(): 
                        kingmoves.remove(kingmoves[i])
                    self.Undo(ox, oy, p, cp, nx, ny) 
        allmoves = self.allMoves()
        if allmoves != 0: #if there are moves the player can make
            for i in range(len(allmoves)-1, -1, -1):
                cp = self.board[allmoves[i][2]][allmoves[i][3]]
                nx = allmoves[i][2]
                ny = allmoves[i][3]
                ox = allmoves[i][0]
                oy = allmoves[i][1]
                p = allmoves[i][4] 
                self.makeMove(nx, ny, ox, oy, p) 
                if self.ifCheck():
                    allmoves.remove(allmoves[i]) 
                self.Undo(ox, oy, p, cp, nx, ny)  
        if len(kingmoves) == 0 and len(allmoves) == 0: #if there is a check and the king has no moves checkmate is true
            self.checkmate = True 

    def ifStalemate(self):
        allmoves = self.allMoves()
        notkingpieces = 0
        for i in range(len(allmoves)):
            if allmoves[i][4][1] != "k":
                notkingpieces += 1
        if notkingpieces == 0: #if there are no pieces that aren't the king it's a stalemate
            self.stalemate = True
        if allmoves != 0: #if there are moves the player can make
            for i in range(len(allmoves)-1, -1, -1):
                cp = self.board[allmoves[i][2]][allmoves[i][3]]
                nx = allmoves[i][2]
                ny = allmoves[i][3]
                ox = allmoves[i][0]
                oy = allmoves[i][1]
                p = allmoves[i][4] 
                self.makeMove(nx, ny, ox, oy, p) 
                if self.ifCheck():
                    allmoves.remove(allmoves[i]) 
                self.Undo(ox, oy, p, cp, nx, ny) 
        if len(allmoves) == 0: #if a player cant move then it's stalemate
            self.stalemate = True
    
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

    def suggestMove(self):
        global new_coordinates, piece_name, original_coordinates
        new_coordinates = None 
        piece_name = None
        original_coordinates = None 
        allmoves = self.allMoves()
        random.shuffle(allmoves) 
        turn = -1
        if self.white: 
            turn = 1
        self.Minimax(allmoves, depth, -checkmate, checkmate, turn) 
        return new_coordinates, piece_name, original_coordinates

    def makeSuggestion(self):
        suggestmove = self.suggestMove() 
        if suggestmove[0] != None and suggestmove[1] != None and suggestmove[2] != None: 
            self.ifCastle()
            self.makeMove(suggestmove[0][0], suggestmove[0][1], suggestmove[2][0], suggestmove[2][1], suggestmove[1]) 
            self.specialMoves(suggestmove[1], suggestmove[0][0], suggestmove[0][1])
            self.white = not self.white
                 
class Piece(): #This stores the properities for a piece that wants to move
    def __init__(self, oldsq, newsq, board):
        self.ox = oldsq[0]
        self.oy = oldsq[1] #old square coordinates
        self.nx = newsq[0]
        self.ny = newsq[1] #new square coordinates
        self.piece = board[self.ox][self.oy] #the piece
    

def loadImages(): 
    for p in range (len(pieces)):
        pieceimage[pieces[p]] = pygame.transform.scale(pygame.image.load("images/" + pieces[p] + ".png"), (50,50))
        
def drawPieces(display,board): 
    for x in range(8):
        for y in range(8):
            piece = board[x][y] 
            if piece != " ":
                if piece in pieceimage: 
                    display.blit(pieceimage[piece], pygame.Rect(x*50, y*50, 50, 50)) 

def drawBoard(display): 
    count = 0
    c1 = pygame.Color("grey")
    c2 = pygame.Color("pink")
    for y in range(8):
        count += 1
        for x in range(8): 
            if count % 2 == 0:
                pygame.draw.rect(display,c2,pygame.Rect(x*50, y*50, 50, 50)) 
            else:
                pygame.draw.rect(display,c1,pygame.Rect(x*50, y*50, 50, 50)) 
            count += 1
          

def highlight(display, row, col): 
    c = pygame.Color("yellow")
    pygame.draw.circle(display, c, ((row*50)+25,(col*50)+25), 15) 

def GameoverText(display, message): 
    font = pygame.font.SysFont("Arial", 24, True, False) 
    text = font.render(message, 0, pygame.Color('Red'))
    area = pygame.Rect(150,175,0,0) 
    display.blit(text, area) 

def main(): 
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s)) 
    clock = pygame.time.Clock()
    state = State()
    display.fill(pygame.Color("white")) 
    run = True
    click = 0
    loadImages() 
    while run:
        for i in pygame.event.get():
            if i.type == pygame.QUIT: #check if the game has been quit out of 
                run = False
            elif i.type == MOUSEBUTTONDOWN: #if mouse has been clicked
                if i.button == 1:
                    click += 1
                    mx,my = pygame.mouse.get_pos() 
                    row = mx//50
                    col = my//50
                    if click == 1: #to select on a piece
                        old = (row, col)
                        p = state.board[row][col]
                        if p[0] == "w":
                            highlight(display, row, col) 
                    if click == 2: #then it moves a piece if theres 2 clicks
                        new = (row, col)
                        object = Piece(old, new, state.board) 
                        state.movePiece(object, display) 
                        click = 0 
                        if state.white == False:
                            state.makeSuggestion()
        clock.tick(30) 
        pygame.display.flip() #updates display
        drawBoard(display) 
        drawPieces(display,state.board) 
        state.ifCheckmate()
        state.ifStalemate()
        if state.checkmate:
            if state.white:
                GameoverText(display, "Black wins")
            else:
                GameoverText(display, "White wins")
        elif state.stalemate:
            GameoverText(display, "Draw")
depth = 3
checkmate = 9999
stalemate = 0
pieces = ["bp","br","bn","bb","bq","bk","wp","wr","wn","wb","wq","wk"]   
pieceimage = {}
main()



