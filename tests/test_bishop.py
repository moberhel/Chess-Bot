from main import State
from main import Piece
import pygame

class TestBishop():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s))
    state = State()
    state.board = [
        [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," ","wb","wb","wb","wb"," "," "],
            [" "," "," "," "," "," "," "," "]
    ]
    
    def test_Bishop1(self):
        self.state.white = True
        old = (6,2)
        new = (3,5)
        piece = self.state.board[old[0]][old[1]]
        bishop = Piece(old, new, self.state.board) 
        self.state.movePiece(bishop, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Bishop2(self):
        self.state.white = True
        old = (6,3)
        new = (3,0)
        piece = self.state.board[old[0]][old[1]]
        bishop = Piece(old, new, self.state.board) 
        self.state.movePiece(bishop, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Bishop3(self):
        self.state.white = True
        old = (6,4)
        new = (7,5)
        piece = self.state.board[old[0]][old[1]]
        bishop = Piece(old, new, self.state.board) 
        self.state.movePiece(bishop, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Bishop4(self):
        self.state.white = True
        old = (6,5)
        new = (7,4)
        piece = self.state.board[old[0]][old[1]]
        bishop = Piece(old, new, self.state.board) 
        self.state.movePiece(bishop, self.display)
        assert self.state.board[new[0]][new[1]] == piece