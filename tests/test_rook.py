from main import State
from main import Piece
import pygame

class TestRook():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s))
    state = State()
    state.board = [
        [" "," "," "," "," "," "," ","wr"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," ","br"," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," ","br"," "," "," "," "," "],
            [" "," "," ","wr"," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "]
    ]

    def test_Rook3(self):
        self.state.white = True
        old = (5,3)
        new = (5,0)
        piece = self.state.board[old[0]][old[1]]
        rook = Piece(old, new, self.state.board) 
        self.state.movePiece(rook, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Rook4(self):
        self.state.white = True
        old = (0,7)
        new = (7,7)
        piece = self.state.board[old[0]][old[1]]
        rook = Piece(old, new, self.state.board) 
        self.state.movePiece(rook, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Rook2(self):
        self.state.white = False
        old = (2,4)
        new = (2,7)
        piece = self.state.board[old[0]][old[1]]
        rook = Piece(old, new, self.state.board) 
        self.state.movePiece(rook, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Rook1(self):
        self.state.white = False
        old = (4,2)
        new = (0,2)
        piece = self.state.board[old[0]][old[1]]
        rook = Piece(old, new, self.state.board) 
        self.state.movePiece(rook, self.display)
        assert self.state.board[new[0]][new[1]] == piece