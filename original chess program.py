import pygame
from pygame.constants import MOUSEBUTTONDOWN
import random

class State():
    def __init__(self):
        #I'm using a 2d list to represent the 8x8 board 
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
        self.white = True #turns
        self.wcastle = True #if white can castle
        self.bcastle = True #if black can castle
        self.wk = (7,3) #white king current location
        self.bk = (0,3) #black king current location
        self.wdead = [] #dead piece list for white
        self.bdead = [] #dead piece list for black
        self.checkmate = False #if checkmate has happened
        self.stalemate = False #if stalemate has happened

    def makeMove(self, nx, ny, ox, oy, p): #make a move
        self.board[nx][ny] = p #adds new piece to the square
        self.board[ox][oy] = " " #leaves the old square as blank 
        if p == "wk":
            self.wk = (nx,ny)
        elif p == "bk":
            self.bk = (nx,ny)
 
    def Error(self, x, y, display): #error display
        c = pygame.Color("red")
        pygame.draw.circle(display, c, ((x*50)+25,(y*50)+25), 15) #displays red circle on the moving piece

    def specialMoves(self, p, x, y):
        if p == "wk":
            if self.wcastle and x == 7 and y == 5: #if white trying to castle
                r1 = (7,7) #old coordinates of rook
                r2 = (7,4) #new coordiantes of rook
                self.makeCastle(r1, r2, p) #makea castle
            elif self.wcastle and x == 7 and y == 1:
                r1 = (7,0)
                r2 = (7,2)
                self.makeCastle(r1, r2, p)
        elif p == "bk":
            if self.bcastle and x == 0 and y == 5: #if black trying to castle
                r1 = (0,7)
                r2 = (0,4)
                self.makeCastle(r1, r2, p)
            elif self.bcastle and x == 0 and y == 1:
                r1 = (0,0)
                r2 = (0,2)
                self.makeCastle(r1, r2, p)
        if x == 0 and p == "wp": #if a white pawn has reached the end of the board
            self.pawnPromotion(x, y, p) #promote the pawn
        elif x == 7 and p == "bp": #if a black pawn has reached the end of the board
            self.pawnPromotion(x, y, p)
        if p == "wp" and x+1 == 3 and self.board[x+1][y] == "bp":
            self.board[x+1][y] = " "
        if p == "bp" and x-1 == 4 and self.board[x-1][y] == "wp":
            self.board[x-1][y] = " "
    
    def deadPieces(self, nx, ny):
        if self.board[nx][ny] != " ": #not equal to blank space
            if self.board[nx][ny][0] == "w": #if the piece is white
                self.wdead.append(self.board[nx][ny]) #append to white's dead pieces list
            else:
                self.bdead.append(self.board[nx][ny]) #append to black's dead pieces list
        
    def makeCastle(self, r1, r2, p):
        if p[0] == "w": #if the piece is white
            self.board[r1[0]][r1[1]] = " " #rooks original spot becomes blank
            self.board[r2[0]][r2[1]] = "wr" #rook moves to new spot
            self.wcastle == False #white cannot castle
        else: #for black side
            self.board[r1[0]][r1[1]] = " "
            self.board[r2[0]][r2[1]] = "br"
            self.bcastle == False
    
    def pawnPromotion(self, x, y, p):
        Queen = True #True means that the queen is the piece to be promoted
        if p[0] == "w": #for white pieces
            for i in range(len(self.wdead)): #for every piece in dead list
                if self.wdead[i] != "wp" and  self.wdead[i] != "wq": #pass the pieces if they are a pawn or queen
                    self.board[x][y] = self.wdead[i] #first dead piece is promoted
                    self.wdead.remove(self.wdead[i]) #removed from list
                    Queen = False #queen won't be the piece to be promoted 
                    break
            if Queen:
                self.board[x][y] = "wq" #if only pawns, the queen or nothing died then queen gets promoted
        else: #for black piece
            for i in range(len(self.bdead)):
                if self.bdead[i] != "bp" and self.bdead[i] != "bq":
                    self.board[x][y] = self.bdead[i]
                    self.bdead.remove(self.bdead[i])
                    Queen = False
                    break
            if Queen:
                self.board[x][y] = "bq"             

    def movePiece(self, moveapiece, display): #The action of moving a piece
        self.checkCastle() #checks every turn if we can castle
        moves = [] #list that stores the possible moves the piece that's being moved
        if moveapiece.piece== " ":
            return
        newmove = (moveapiece.nx,moveapiece.ny) #what square the piece is being moved to 
        self.possibleMoves(moveapiece.piece, moveapiece.ox, moveapiece.oy, moves) #checks all the possible moves for that piece
        self.ifCheck() #checks for check
        if ((moveapiece.piece[0] == "w" and self.white == True) or (moveapiece.piece[0] == "b" and self.white == False)) and newmove in moves:
            #checks if it's black or whites turn and if the current move is possible
            self.deadPieces(moveapiece.nx, moveapiece.ny) #if a piece is being captured, it will be put into the dead pieces list
            cp = self.board[moveapiece.nx][moveapiece.ny] #opposing piece 
            self.makeMove(moveapiece.nx,moveapiece.ny, moveapiece.ox, moveapiece.oy, moveapiece.piece) #makes the move
            self.specialMoves(moveapiece.piece, moveapiece.nx, moveapiece.ny) # special moves
            if self.ifCheck(): #if the move causes a check
                self.Undo(moveapiece.ox, moveapiece.oy, moveapiece.piece, cp, moveapiece.nx, moveapiece.ny) #undos move
                self.Error(moveapiece.ox, moveapiece.oy, display) #visually shows an error
                self.white = not self.white #swtiches turns
            self.white = not self.white #swtiches turns    
        else: #if not then show an error
            self.Error(moveapiece.ox, moveapiece.oy, display)

    def possibleMoves(self, p, x, y, moves):
        if p[1] == "p": #if and elif statements check what piece is being called
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
        if p[0] == "w": #white piece
            if x-1 >= 0 and self.board[x-1][y] == " ": #if it can move forward 1 space
                moves.append((x-1,y)) #appends poissible move to list
            if  x == 6 and self.board[x-2][y] == " " and self.board[x-1][y] == " ": #if it can move forward 2 spaces
                moves.append((x-2,y))
            for dy in (-1, 1): #loop that switches between attacking to the right and left
                ny = y + dy #adds index onto current position to find the new position the pawn can go to
                nx = x - 1
                if 0 <= ny <= 7 and self.board[nx][ny][0] == "b": #if it can do a normal pawn capture
                    moves.append((nx, ny))
                if x == 3 and 0 <= ny <= 7 and self.board[x][ny][0] == "b" and self.board[nx][ny][0] == " ": #if it meets all the requirements for en passant
                    moves.append((nx, ny))
        else: #same as comments above but for black piece
            if x+1 <= 7 and self.board[x+1][y] == " ":
                moves.append((x+1, y))
            if x == 1 and self.board[x+2][y] == " " and self.board[x+1][y] == " ":
                moves.append((x+2,y))
            for dy in (-1, 1): 
                ny = y + dy
                nx = x + 1 
                if 0 <= ny <= 7 and self.board[nx][ny][0] == "w":
                    moves.append((nx, ny))
                if x == 4 and 0 <= ny <= 7 and self.board[x][ny][0] == "w" and self.board[nx][ny][0] == " ": #en passant
                    moves.append((nx, ny))

    def Knight(self, p, x, y, moves): #possible moves for a knight
        for (dx, dy) in [(1, -2), (1, 2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]: #loop for all 8 movements the knight can do
            nx = x + dx 
            ny = y + dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]:
                #if the knight can move to one of the directions also checks if the new square isn't out of the board
                moves.append((nx,ny))
            else:
                pass

    def Rook(self, p, x, y, moves): #possible moves for a bishop
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]: #all 4 horizontal and vertical directions the rook can move to
            for i in range(1, 8): #loop to check every poissble square (8 at most) the rook can move to
                nx = x + dx*i #since the rook can go to multiple spaces in 1 direction, we multiple the index by the direction we want to go to and add it to old space coordinates.
                ny = y + dy*i
                if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]: #if the rook can move to the new square
                    moves.append((nx,ny))
                    if self.board[nx][ny][0] != " ": #if there's a piece (assumed to be black) in the way then break out of the loop and check a new direction 
                        break
                else:
                    break #breaks the loop if the same colored piece is in the way and check a new direction 

    def Bishop(self, p, x, y, moves): #possible moves for a rook
        for (dx, dy) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]: #all 4 diagonal directions the bishop can move to
                for i in range(1, 8):
                    nx = x + dx*i
                    ny = y + dy*i
                    if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]: #if the bishop can move to the new square
                        moves.append((nx,ny))
                        if self.board[nx][ny][0] != " ":
                            break
                    else:
                        break

    def King(self, p, x, y, moves): #possible moves for a king
        if p[0] == "w":
            if self.wcastle and self.board[7][6] == " " and self.board[7][5] == " " and self.board[7][4] == " ":
                #if all the condtions are met for white king side castle
                moves.append((7,5))
            elif self.wcastle and self.board[7][1] == " " and self.board[7][2] == " ":
                #if all the condtions are met for white queen side castle
                moves.append((7,1))
        else:
            if self.bcastle and self.board[0][6] == " " and self.board[0][5] == " " and self.board[0][4] == " ":
                #if all the condtions are met for black king side castle
                moves.append((0,5))
            elif self.bcastle and self.board[0][1] == " " and self.board[0][2] == " ":
                #if all the condtions are met for black queen side castle
                moves.append((0,1))
        for (dx, dy) in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]: #all 8 directions the king can move to
            nx = x + dx
            ny = y + dy
            if 0 <= nx <= 7 and 0 <= ny <= 7 and self.board[nx][ny][0] != p[0]:
                moves.append((nx,ny))
                if self.board[nx][ny][0] != " ":
                    pass
            else:
                pass

    def checkCastle(self): #function basically checks if the king has ever been moved before
        if self.board[7][3] != "wk" or self.board[7][7] != "wr" or self.board[7][0] != "wr":
            self.wcastle = False #castle is set to false when king has been moved
        if self.board[0][3] != "bk" or self.board[0][7] != "br" or self.board[0][0] != "br":
            self.bcastle = False
 
    def Undo(self, x, y, p, cp, nx, ny):
        self.board[x][y] = p
        self.board[nx][ny] = cp #the pieces position are swapped back to before
        if p == "wk":
            self.wk = (x, y) #if a king was moved then the original coordinates go back to normal
        elif p == "bk":
            self.bk = (x, y)
        

    def ifCheck(self):  
        if self.white: #on white's turn
            return self.ifCapturing(self.wk[0], self.wk[1]) #calls ifCapturing functions using white king's coordinates
        else: #for black's turn
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
            side = "w" #for white pieces
        else:
            side = "b" #for black pieces
        for y in range(8):
            for x in range(8): #for every square on the board
                piecemoves = []
                p = self.board[x][y] #current piece
                if p[0] == side:
                    self.possibleMoves(p, x, y, piecemoves) #finds possible moves for the piece
                    for move in piecemoves: #for each move for that piece's moves
                        allmoves.append((x, y, move[0], move[1], self.board[x][y], 
                        self.board[move[0]][move[1]])) #append it to all moves with captured piece, coordinates before and after
        return allmoves

    def ifCheckmate(self): 
        kingmoves = []
        if self.white:
            self.King("wk", self.wk[0], self.wk[1], kingmoves)
            p = "wk"
            ox = self.wk[0]
            oy = self.wk[1] #sets up variables for white king
        else:
            self.King("bk", self.bk[0], self.bk[1], kingmoves)
            p = "bk"
            ox = self.bk[0]
            oy = self.bk[1] #sets up variables for black king
        if self.ifCheck():
            if kingmoves != 0: #if there's a move that the king can move to
                for i in range(len(kingmoves)-1, -1, -1): #goes from the back of the list
                    cp = self.board[kingmoves[i][0]][kingmoves[i][1]]
                    nx = kingmoves[i][0]
                    ny = kingmoves[i][1]
                    self.makeMove(nx, ny, ox, oy, p) #makes a move for each of the king's moves
                    if self.ifCheck(): #if it causes check remove it from the list
                        kingmoves.remove(kingmoves[i])
                    self.Undo(ox, oy, p, cp, nx, ny) #undo moveallmoves = self.allMoves()
        allmoves = self.allMoves()
        if allmoves != 0: #if there are moves
            for i in range(len(allmoves)-1, -1, -1):
                cp = self.board[allmoves[i][2]][allmoves[i][3]]
                nx = allmoves[i][2]
                ny = allmoves[i][3]
                ox = allmoves[i][0]
                oy = allmoves[i][1]
                p = allmoves[i][4] #variables for make move
                self.makeMove(nx, ny, ox, oy, p) #makes a move
                if self.ifCheck():
                    allmoves.remove(allmoves[i]) #if it causes a check then remove from list
                self.Undo(ox, oy, p, cp, nx, ny) #undos the move  
        if len(kingmoves) == 0 and len(allmoves) == 0: #if there is a check and the king has no moves 
            self.checkmate = True #checkmate is true

    def ifStalemate(self):
        allmoves = self.allMoves()
        if allmoves != 0: #if there are moves
            for i in range(len(allmoves)-1, -1, -1):
                cp = self.board[allmoves[i][2]][allmoves[i][3]]
                nx = allmoves[i][2]
                ny = allmoves[i][3]
                ox = allmoves[i][0]
                oy = allmoves[i][1]
                p = allmoves[i][4] #variables for make move
                self.makeMove(nx, ny, ox, oy, p) #makes a move
                if self.ifCheck():
                    allmoves.remove(allmoves[i]) #if it causes a check then remove from list
                self.Undo(ox, oy, p, cp, nx, ny) #undos the move
        if len(allmoves) == 0: #if a player cant move then it's stalemate
            self.stalemate = True
    
    def scoreBoard(self):
        piecevalue = {"k": 0, "q": 9, "r": 5, "n": 3, "b": 3, "p": 1} #value for each piece
        knightScores = [[1, 1, 1, 1, 1, 1, 1, 1], #position scores for knight
                        [1, 1, 2, 2, 2, 2, 1, 1],
                        [1, 2, 2, 3, 3, 2, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 2, 3, 3, 2, 2, 1],
                        [1, 1, 2, 2, 2, 2, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1]
                        ]
        bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4], #position scores for bishop
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [4, 3, 2, 1, 1, 2, 3, 4]
                        ]
        queenScores = [[1, 1, 1, 3, 3, 1, 1, 1], #position scores for queen
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 1, 1, 3, 3, 1, 1, 1]
                       ]
        rookScores = [[4, 3, 4, 4, 4, 4, 3, 4], #position scores for rook
                      [4, 4, 4, 4, 4, 4, 4, 4],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [4, 4, 4, 4, 4, 4, 4, 4],
                      [4, 3, 4, 4, 4, 4, 3, 4]
                      ]
        whitepawnScores = [[8, 8, 8, 8, 8, 8, 8, 8], #position scores for white pawn
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [4, 4, 5, 5, 5, 5, 4, 4],
                           [2, 3, 4, 4, 4, 4, 3, 2],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 1, 2, 3, 3, 2, 2, 1],
                           [1, 1, 1, 0, 0, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0]
                           ]
        whitekingScores = [[1, 1, 1, 1, 1, 1, 1, 1], #position scores for white king
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [2, 1, 1, 1, 1, 1, 1, 2],
                           [2, 2, 1, 1, 1, 1, 2, 2],
                           [2, 2, 2, 1, 1, 2, 2, 2],
                           [3, 3, 2, 2, 2, 2, 3, 3],
                           [4, 5, 4, 3, 3, 4, 5, 4],
                           ]
        blackkingScores = [[4, 5, 4, 3, 3, 4, 5, 4], #position scores for black king
                           [3, 3, 2, 2, 2, 2, 3, 3],
                           [2, 2, 2, 1, 1, 2, 2, 2],
                           [2, 2, 1, 1, 1, 1, 2, 2],
                           [2, 1, 1, 1, 1, 1, 1, 2],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1]
                           ]
        blackpawnScores = [[0, 0, 0, 0, 0, 0, 0, 0], #position scores for black pawn
                           [1, 1, 1, 0, 0, 1, 1, 1],
                           [1, 1, 2, 3, 3, 2, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [2, 3, 4, 4, 4, 4, 3, 2],
                           [4, 4, 5, 5, 5, 5, 4, 4],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [8, 8, 8, 8, 8, 8, 8, 8]
                           ]
        positionScores = {"n": knightScores, "q": queenScores, "b": bishopScores, "r": rookScores, "bp": blackpawnScores, "wp": whitepawnScores,
                          "bk": blackkingScores, "wk": whitekingScores} #links the lists to their values
        totalScore = 0
        positionScore = 0 
        if self.checkmate: #for checkmate
            if self.white:
                return -checkmate
            else:
                return checkmate
        elif self.stalemate: #for stalemate
            return stalemate
        for x in range(8):
            for y in range(8): #searches every square on the board
                if self.board[x][y] != " ":
                    if self.board[x][y][1] == "n": #if statements to check what piece it's for
                        positionScore = positionScores["n"][x][y] #adds score
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
                        totalScore += piecevalue[self.board[x][y][1]] + positionScore*0.5 #adds the calculated score to the total score
                    elif self.board[x][y][0] == "b":
                        totalScore -= piecevalue[self.board[x][y][1]] + positionScore*0.5 #black is negative to represent the other side
        return totalScore #returns total score. If total score is positive, it's winning for white and vice versa
            
    def Minimax(self, moves, d, alpha, beta, turn):
        global new_coordinates, piece_name, original_coordinates
        if d == 0:
            return turn * self.scoreBoard() #returns the final score if the depth is 0
        maxScore = -checkmate #maxScore is set to negative infinity (-9999)
        for move in moves: 
            self.makeMove(move[2], move[3], move[0], move[1], move[4]) #a move is made for every move in moves
            if self.ifCheck():
                self.Undo(move[0], move[1], move[4], move[5], move[2], move[3])
                continue
            self.white = not self.white
            nextmoves = self.allMoves() #finds the next set of moves for the other side
            score = -self.Minimax(nextmoves, d-1, -beta, -alpha, -turn) #minimax but for their side
            if score > maxScore:
                maxScore = score #set the maxScore to the current score if it's higher than the previous score
                if d == depth:
                    new_coordinates = (move[2], move[3]) #these variables contains the properities for the current best move found
                    piece_name = self.board[move[2]][move[3]]
                    original_coordinates = (move[0], move[1])
            self.Undo(move[0], move[1], move[4], move[5], move[2], move[3]) #undos move
            self.white = not self.white
            if maxScore > alpha: #alpha beta pruning 
                alpha = maxScore #sets alpha to the maxScore
            if alpha >= beta: #if alpha is higher than beta the function doesn't need to check the beta's path
                break #breaks out of the loop since it knows it won't find a higher score than alpha
        return maxScore

    def suggestMove(self):
        global new_coordinates, piece_name, original_coordinates
        new_coordinates = None #new coordinates
        piece_name = None
        original_coordinates = None #old coordinates
        allmoves = self.allMoves() #gets every move
        random.shuffle(allmoves) #shuffles the move list
        turn = -1
        if self.white: #if it's white's or black's turn
            turn = 1
        self.Minimax(allmoves, depth, -checkmate, checkmate, turn) #calls minimax function
        return new_coordinates, piece_name, original_coordinates

    def makeSuggestion(self):
        suggestmove = self.suggestMove() #gets the suggestion
        if suggestmove[0] != None and suggestmove[1] != None and suggestmove[2] != None: #if there is a suggestion is not nothing
            self.makeMove(suggestmove[0][0], suggestmove[0][1], suggestmove[2][0], suggestmove[2][1], suggestmove[1]) #does the suggested move
            self.white = not self.white
                 
class Piece(): #This stores the properities for a piece that wants to move
    def __init__(self, oldsq, newsq, board):
        self.ox = oldsq[0]
        self.oy = oldsq[1] #old square coordinates
        self.nx = newsq[0]
        self.ny = newsq[1] #new square coordinates
        self.piece = board[self.ox][self.oy] #the piece
    

def loadImages(): #loads the images
    for p in range (len(pieces)):
        pieceimage[pieces[p]] = pygame.transform.scale(pygame.image.load("images/" + pieces[p] + ".png"), (50,50))
        #scales and loads the images by using an exisitng list called pieces and putting in into images

def drawPieces(display,board): #draws the pieces
    for x in range(8):
        for y in range(8):
            piece = board[x][y] #finding out what piece is supposed to be in a position of the board
            if piece != " ":
                if piece in pieceimage: #finding the index of the piece in pieces
                    display.blit(pieceimage[piece], pygame.Rect(x*50, y*50, 50, 50)) #displays the image in the correct position

def drawBoard(display): #draws the board
    count = 0
    c1 = pygame.Color("grey")
    c2 = pygame.Color("pink")#two different colors
    for y in range(8):
        count += 1
        for x in range(8): #board is 8x8 so we go through all the squares
            if count % 2 == 0:
                pygame.draw.rect(display,c2,pygame.Rect(x*50, y*50, 50, 50)) #draws grey square
            else:
                pygame.draw.rect(display,c1,pygame.Rect(x*50, y*50, 50, 50)) #draws pink square
            count += 1
            #black and white squares

def highlight(display, row, col): #indicator to show that a piece has been clicked on
    c = pygame.Color("yellow")
    pygame.draw.circle(display, c, ((row*50)+25,(col*50)+25), 15) #yellow circle that fits within a square of the piece being moved

def GameoverText(display, message): #sets up game over text
    font = pygame.font.SysFont("Arial", 24, True, False) 
    text = font.render(message, 0, pygame.Color('Red'))
    area = pygame.Rect(150,175,0,0) 
    display.blit(text, area) 

def main(): #the main function
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") #the game is called Chess
    s = 400
    display = pygame.display.set_mode((s, s)) #400x400 screen
    clock = pygame.time.Clock() #sets up time 
    state = State()
    display.fill(pygame.Color("white")) #background is white
    run = True
    click = 0
    whitesm = 3
    blacksm = 3
    loadImages() #loads the images from the list pieces
    while run:
        for i in pygame.event.get():
            if i.type == pygame.QUIT: #check if the game has been quit out of 
                run = False
            elif i.type == MOUSEBUTTONDOWN: #if mouse has been clicked
                if i.button == 1:
                    click += 1
                    mx,my = pygame.mouse.get_pos() #gets the coordinates of the mouse and divides it by 50 to find the square
                    row = mx//50
                    col = my//50
                    if click == 1: #to select on a piece
                        old = (row, col)
                        p = state.board[row][col]
                        if p[0] != " ":
                            highlight(display, row, col) #highlights
                    if click == 2: #then it moves a piece if theres 2 clicks
                        new = (row, col)
                        object = Piece(old, new, state.board) #creates new object
                        state.movePiece(object, display) #moves the piece
                        click = 0 #reset the clicks
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_b:
                    if state.white == True and whitesm != 0:
                        state.makeSuggestion()
                        whitesm -= 1
                    elif state.white == False and blacksm != 0:
                        state.makeSuggestion()
                        blacksm -= 1
        clock.tick(15) #15 frames every second
        pygame.display.flip() #updates display
        drawBoard(display) #sets up and updates the board
        drawPieces(display,state.board) #sets up and updates the pieces
        state.ifCheckmate()
        state.ifStalemate()
        if state.checkmate:
            if state.white:
                GameoverText(display, "Black wins")
            else:
                GameoverText(display, "White wins")
            whitesm = 0
            blacksm = 0
        elif state.stalemate:
            GameoverText(display, "Draw")
            whitesm = 0
            blacksm = 0
depth = 3
checkmate = 9999
stalemate = 0
pieces = ["bp","br","bn","bb","bq","bk","wp","wr","wn","wb","wq","wk"]   
pieceimage = {}
main()



