from main import State
from main import Piece
import pygame

class TestPawn():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s))
    state = State()
    state.board = [
        [" "," "," "," "," "," "," "," "],
            ["wp"," "," "," "," "," ","bp","bp"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," ","bp","wp"," "," "],
            ["bp","wp"," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," ","bp"," "," "," ","wp","wp"],
            [" "," "," "," "," "," "," "," "]
    ]
    state.wk = (0,0)
    state.bk = (7,7)

    def test_Pawn6(self):
        self.state.white = True
        old = (6,6)
        new = (5,6)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Pawn1(self):
        self.state.white = True
        old = (6,7)
        new = (4,7)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece 

    def test_Pawn2(self):
        self.state.white = False
        old = (1,6)
        new = (2,6)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Pawn3(self):
        self.state.white = True
        old = (3,5)
        new = (2,4)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Pawn4(self):
        self.state.white = False
        old = (6,2)
        new = (7,2)
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == "bq"

    def test_Pawn5(self):
        self.state.white = False
        old = (1,7)
        new = (3,7)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece 

    def test_Pawn7(self):
        self.state.white = False
        old = (4,0)
        new = (5,1)
        piece = self.state.board[old[0]][old[1]]
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Pawn8(self):
        self.state.white = True
        old = (1,0)
        new = (0,0)
        pawn = Piece(old, new, self.state.board) 
        self.state.movePiece(pawn, self.display)
        assert self.state.board[new[0]][new[1]] == "wq"